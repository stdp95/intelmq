# -*- coding: utf-8 -*-

import hashlib
import gevent
import requests

import gevent.monkey
gevent.monkey.patch_socket()
from gevent.pool import Pool

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache


class RblCheckExpertBot(Bot):

    def init(self):
        
        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           self.parameters.redis_cache_ttl,
                           getattr(self.parameters, "redis_cache_password",
                                   None)
                           )
        self.pool = Pool(self.parameters.pool_size)
        self.timeout = getattr(self.parameters, "timeout", None)
        self.lifetime = getattr(self.parameters, "lifetime", None)
        self.set_request_parameters()
        self.service_url = getattr(self.parameters, 'service_url', 'http://127.0.0.1:5000/api/v1/lookup/short/')

    def process(self):
        self.pool.spawn(self._process)


    def query(self, url):
        lookup_url = self.service_url + url
            
        result = requests.get(lookup_url, 
                                proxies=self.proxy,
                                headers=self.http_header,
                                verify=self.http_verify_cert,
                                cert=self.ssl_client_cert)
        if result.status_code != 200:
            return None
        try:
           return result.json()
        except:
            return []

    def _process(self):
        event = self.receive_message()
       
        for key in ['source.', 'destination.']:
            ip_key = key + "ip"
            fqdn_key = key + "fqdn"
            ip = event.get(ip_key, None)
            fqdn = event.get(fqdn_key, None)
                      
            if ip:
                cache_key = hashlib.md5(ip.encode('utf-8')).hexdigest()
                cachevalue = self.cache.get(cache_key)
                response = []
                if cachevalue:
                    response = cachevalue
                else:
                    response = self.query(ip)
                    self.cache.set(cache_key, str(response), ttl = 60)
                event.add("extra.%s.in_dnsfw" % ip_key, response.get("in_dnsfw"))
                event.add("extra.%s.in_rbl" % ip_key, response.get("in_rbl"))
            if fqdn:
                cache_key = hashlib.md5(fqdn.encode('utf-8')).hexdigest()
                cachevalue = self.cache.get(cache_key)
                result = []
                if cachevalue:
                    result = cachevalue
                else:
                    response = self.query(fqdn)
                    self.cache.set(cache_key, str(response), ttl = 60)
                event.add("extra.%s.in_rbl", response.get["in_rbl"])
                event.add("extra.%s.in_dnsfw", response.get["in_dnsfw"])
                

        self.send_message(event)
        self.acknowledge_message()


BOT = RblCheckExpertBot
