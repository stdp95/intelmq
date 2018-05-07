# -*- coding: utf-8 -*-
from dateutil import parser
import json

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from collections import OrderedDict


class TalosParserBot(ParserBot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        feed = json.loads(raw_report, object_pairs_hook=OrderedDict)

        for item in feed['data'][0]:
            event = self.new_event(report)
            if 'hostname' in item:
                event.add('source.fqdn', item['hostname'], raise_failure=False)
            if 'ip' in item:
                event.add('source.ip', item['ip'])
            event.add('classification.type', 'malware')
            event.add('raw', json.dumps(item))
            self.send_message(event)
        self.acknowledge_message()


BOT = TalosParserBot
