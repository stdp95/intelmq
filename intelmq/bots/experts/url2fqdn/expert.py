# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from intelmq.lib.bot import Bot


class Url2fqdnExpertBot(Bot):

    def init(self):
        self.overwrite = getattr(self.parameters, 'overwrite', False)

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:

            key_url = key + "url"
            key_fqdn = key + "fqdn"
            key_path = key + "urlpath"
            if key_url not in event:
                continue
            if key_path in event and not self.overwrite:
                continue
            if key_fqdn in event and not self.overwrite:
                continue

            url = urlparse(event.get(key_url))

            event.add("source.ip", url.hostname, overwrite=True, raise_failure=False)
            event.add(key_fqdn, url.hostname, overwrite=True, raise_failure=False)
            event.add(key_path, url.path, overwrite=True, raise_failure=False)

        self.send_message(event)
        self.acknowledge_message()


BOT = Url2fqdnExpertBot
