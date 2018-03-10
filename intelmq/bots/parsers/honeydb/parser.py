# -*- coding: utf-8 -*-
"""
"""

import json
from dateutil import parser

from intelmq.lib import utils
from intelmq.lib.bot import Bot

class HoneydbParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get('raw'))

        for item in json.loads(raw_report):
            event = self.new_event(report)
            if 'remote_host' in item:
                event.add('source.ip', item['remote_host'])
            if 'last_seen' in item:
                event.add('time.source', parser.parse(item['last_seen']).isoformat()+"UTC")
            event.add("classification.type", 'scanner')
            event.add("raw", json.dumps(item, sort_keys=True))  # sorting for undefined order
            self.send_message(event)
        self.acknowledge_message()


BOT = HoneydbParserBot
