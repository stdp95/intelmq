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
            if key.startswith('feed.'):
                continue
            if key.startswith('classification.'):
                continue
            if key.startswith('event.'):
                continue
            if key.startswith('event_description.'):
                continue
            if key.endswith('.ip'):
                ioc_types.add('ip')
            if key.endswith('.fqdn'):
                ioc_types.add('domain')
            if key.endswith('.url'):
                ioc_types.add('url')
            if key.startswith('malware.hash'):
                ioc_types.add('hash')
        if 'extra' in event:
            extra = event['extra']
            if isinstance(extra, str):
                try:
                    extra = json.loads(extra)
                except:
                    pass
            extra['ioc_types'] = list(ioc_types)
            event.change('extra', extra)
        else:
            event.add('extra', {'ioc_types': list(ioc_types)})
        self.send_message(event)
        self.acknowledge_message()


BOT = IOCExpertBot
