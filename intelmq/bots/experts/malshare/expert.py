# -*- coding: utf-8 -*-
import requests
import json

from intelmq.lib.bot import Bot
from intelmq.lib import utils


class MalShareExpertBot(Bot):

    def process(self):
        message = self.receive_message()
        hash = message.get("malware.hash.md5")
        data = requests.get(url="https://malshare.com/api.php?api_key=7523014f80764ae82afffb519fd73fc20d851i2"
                            "e158ad622af3fa3e903e4b12bd&action=details&hash=%s" % (hash))
        feed = json.loads(data.content.decode('utf-8'))
        if "SHA1" in feed:
            message.add("malware.hash.sha1", feed["SHA1"])
        if "SHA256" in feed:
            message.add("malware.hash.sha256", feed["SHA256"])
        if "SOURCES" in feed:
            for source in feed["SOURCES"]:
                message.add("source.url", source, overwrite=True, raise_failure=False)
                self.send_message(message)
        self.acknowledge_message()


BOT = MalShareExpertBot
