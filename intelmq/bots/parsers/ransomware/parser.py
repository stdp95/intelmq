# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from intelmq.lib.bot import ParserBot


class RansomwareParserBot(ParserBot):

    parse = ParserBot.parse_csv
    recover_line = ParserBot.recover_line_csv

    def parse_line(self, row, report):

        event = self.new_event(report)
        if row[0].startswith("#"):
            return
        event.add("raw", self.recover_line(row))
        event.add("time.source", row[0] + "UTC")
        event.add("malware.name", row[2].lower())
        event.add("source.url", row[4])
        event.add('classification.type', 'malware')
        ips = set([ip for ip in row[7].split('|') if len(ip) > 7])
        for ip in ips:
            added = event.add("source.ip", ip, raise_failure=False, overwrite=True)
            self.send_message(event)
        else:
            self.send_message(event)
        self.acknowledge_message()


BOT = RansomwareParserBot
