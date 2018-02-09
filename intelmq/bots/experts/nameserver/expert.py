# -*- coding: utf-8 -*-

import hashlib
import gevent
import dns

from json import loads, dumps
from collections.abc import Mapping
from datetime import datetime
from dns import resolver
import gevent.monkey
gevent.monkey.patch_socket()
from gevent.pool import Pool

from intelmq.lib.bot import Bot
from intelmq.lib.cache import Cache

DNS_EXCEPTION_VALUE = "__dns-exception"


class ReverseDnsExpertBot(Bot):

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
        self.resolver = resolver.Resolver()
        if self.timeout:
            self.resolver.timeout = self.timeout
        if self.lifetime:
            self.resolver.lifetime = self.lifetime

    def process(self):
        self.pool.spawn(self._process)

    def _process(self):
        event = self.receive_message()

        keys = ["source.%s", "destination.%s"]

        for key in keys:
            fqdn_key = key % "fqdn"

            if fqdn_key not in event:
                continue

            fqdn = event.get(fqdn_key)

            cache_key = hashlib.md5(fqdn_key.encode('utf-8')).hexdigest()
            cachevalue = self.cache.get(cache_key)

            result = None
            if cachevalue == DNS_EXCEPTION_VALUE:
                continue
            elif cachevalue:
                result = cachevalue
            else:
                try:
                    result = self.resolver.query(fqdn, "NS")
                    expiration = result.expiration
                    items = result.response.answer[0].items
                    result = [i.to_text() for i in items]
                except (dns.exception.DNSException, ValueError) as e:
                    # Set default TTL for 'DNS query name does not exist' error
                    ttl = None if isinstance(e, dns.resolver.NXDOMAIN) else \
                        getattr(self.parameters, "cache_ttl_invalid_response",
                                60)
                    self.cache.set(cache_key, DNS_EXCEPTION_VALUE, ttl)

                else:
                    ttl = datetime.fromtimestamp(expiration) - datetime.now()
                    self.cache.set(cache_key, str(result),
                                   ttl=int(ttl.total_seconds()))

            if result is not None:
                if 'extra' in event:
                    extra = event['extra']
                    if isinstance(extra, str):
                            try:
                                extra = loads(extra)
                            except:
                                pass
                    if isinstance(extra, Mapping):
                        extra[key % 'nameservers'] = result
                        event.change('extra', extra)

                else:
                    event.add('extra', {key % 'nameserver': result})

        self.send_message(event)
        self.acknowledge_message()


BOT = ReverseDnsExpertBot
