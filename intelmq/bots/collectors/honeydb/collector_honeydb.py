# -*- coding: utf-8 -*-
import json

from intelmq.lib.bot import CollectorBot

try:
    from honeydb import api
except ImportError:
    api = None


class HoneydbCollectorBot(CollectorBot):
    def init(self):
        if api is None:
            self.logger.error('Could not import honeydb.api. Please install it.')
            self.stop()

    def process(self):
        self.logger.debug("Downloading report through API.")
        honeyapi =  api.Client(self.parameters.api_id, self.parameters.api_key)

        response = honeyapi.bad_hosts()
        self.logger.info("Report downloaded.")

        report = self.new_report()
        report.add("raw", json.dumps(response))
        self.send_message(report)


BOT = HoneydbCollectorBot
