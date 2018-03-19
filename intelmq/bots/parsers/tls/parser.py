# -*- coding: utf-8 -*-
import json

from intelmq.lib.bot import Bot
from intelmq.lib import utils

ioc =['ip','fqdn','url','network']




class TlsParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get("raw"))
        item = json.loads(raw_report)

        for data in item:
            event = self.new_event(report)
            event.add('classification.type','malware')
            event.add('classification.taxonomy','malacious code')
            if 'source_type' in data:
                event.add('extra', {"source_type": data['source_type']})
            if 'ioc_type' in data:
                ioc_type = data['ioc_type']
                if ioc_type in ioc:
                   event.add('source.%s'%(ioc_type),data['value'])
            if 'time_source' in data:
                dt = data['time_source'] + " UTC"
                event.add('time.source', dt)
            event.add('raw',json.dumps(data))

            self.send_message(event)

        self.acknowledge_message()


BOT = TlsParserBot
