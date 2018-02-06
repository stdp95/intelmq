# -*- coding: utf-8 -*-
"""
Add current time in extra fields
"""
import socket

from json import loads, dumps
from collections.abc import Mapping
from datetime import datetime as dt

from intelmq.lib.bot import Bot


class HostnameExpertBot(Bot):

    def init(self):
        hostname = socket.gethostname()
        self.hostname = getattr(self.parameters, 'hostname',  None)
        if self.hostname is None:
            self.hostname = hostname

    def process(self):
        event = self.receive_message()
        if 'extra' in event:
            extra = event['extra']
            if isinstance(extra, str):
                    try:
                        extra = loads(extra)
                    except:
                        pass
            if isinstance(extra, Mapping):
                extra['hostname'] = self.hostname
            # oddity existing extra value is string and we dont know the key
            # how do we handle this?
            else:
                extra = {"extra": extra,
                         "hostname": self.hostname}
            event.change('extra', extra)

        else:   # no extra add extra
            event.add('extra', {'hostname': self.hostname})
        self.send_message(event)
        self.acknowledge_message()


BOT = HostnameExpertBot
