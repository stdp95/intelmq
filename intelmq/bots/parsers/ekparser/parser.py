# -*- coding: utf-8 -*-
import json

from intelmq.lib.bot import Bot
from intelmq.lib import utils
from  collections import OrderedDict


class EkParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))
        required = {'tags', 'url', 'timestamp'}
        item = json.loads(raw_report,object_pairs_hook=OrderedDict)

        for data in item['data']:
            event = self.new_event(report)
            event.add('classification.type','malware')
            #event.add('classification.taxonomy','malacious code')
            if 'tags' in data:
                event.add('extra', {"tags": data['tags']})
            if 'url' in data:
                url = data['url']
                url = url.replace('[', '') if '[' in url else url
                url = url.replace(']', '') if ']' in url else url
                if url.startswith('http://'):
                    event.add('source.url', url)
                else:
                    event.add('source.ip', url)
            if 'timestamp' in data:
                dt = data['timestamp'] + " UTC"
                event.add('time.source', dt)
            event.add('raw',json.dumps(data))

            self.send_message(event)

        self.acknowledge_message()


BOT = EkParserBot
