# -*- coding: utf-8 -*-
"""
IOC expert bot adds ioc array in extra.ioc_type
"""

import json

from intelmq.lib.bot import Bot


class IOCExpertBot(Bot):

    def process(self):
        ioc_types = set()
        event = self.receive_message()
        for key in event:
            if key.endswith('.ip'):
                ioc_types.add('ip')
            if key.endswith('.fqdn'):
                ioc_types.add('domain')
            if key.endswith('.url'):
                ioc_types.add('url')
            if key.startswith('malware.hash'):
                ioc_types.add('hash')
        if 'extra' in event:
            extra = json.loads(event['extra'])
            extra['ioc_types'] = list(ioc_types)
            event.change('extra', extra)
        else:
            event.add('extra', {'ioc_types': list(ioc_types)})
        self.send_message(event)
        self.acknowledge_message()


BOT = IOCExpertBot
