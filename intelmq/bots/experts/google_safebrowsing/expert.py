# -*- coding: utf-8 -*-
from urllib.parse import quote_plus

import requests

from intelmq.lib.bot import Bot


STATUS_CODE_ERROR = 'HTTP status code was %s. Possible problem at the connection endpoint or network issue.'


class GSBExpertBot(Bot):

    def init(self):
        self.service_url = getattr(self.parameters, 'service_url', 'http://127.0.0.1:5000/gglsbl/lookup/')
        self.set_request_parameters()

    def query_gsb(self, url):
        lookup_url = self.service_url + quote_plus(url)
        response = requests.get(lookup_url, 
                                proxies=self.proxy,
                                headers=self.http_header,
                                verify=self.http_verify_cert,
                                cert=self.ssl_client_cert,
                                timeout=self.http_timeout_sec)
        if response.status_code != 200:
            return None

        threat_lists = [i['threat'] for i in response.json()['matches']]
        return list(set(threat_lists))
        try:
            threat_lists = [i['threat'] for i in response.json()['matches']]
            return list(set(threat_lists))
        except:
            return []

    def process(self):
        event = self.receive_message()

        for key in ['source.', 'destination.']:
            url_key = key + "url"
            fqdn_key = key + "fqdn"

            url = event.get(url_key, None)
            fqdn = event.get(fqdn_key, None)
            if not url and not fqdn:
                continue
            if not url and fqdn:
                url = 'http://'+fqdn

            response = self.query_gsb(url)

            if response:
                #event.add("extra.%sgsb_blacklisted" % key, True)
                event.add("extra.%sgsb_tags" % key, response)

        self.send_message(event)
        self.acknowledge_message()


BOT = GSBExpertBot
