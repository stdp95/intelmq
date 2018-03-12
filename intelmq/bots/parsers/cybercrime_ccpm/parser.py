# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from dateutil import parser

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class CybercrimeParserBot(ParserBot):
    def init(self):
        self.tags = []
        self.raw = ''
        self.info = []

    def parse(self, soup):
        for td in soup.findAll('td', attrs={'align': "MIDDLE"}):
            if td.text != " ":
                self.info.append(td.text)
                self.raw += '%s' % (td)
                if len(self.info) % 5 == 0:
                    self.tags.append(self.info)
                    self.tags[len(self.tags) - 1].append(self.raw)
                    self.raw = ''
                    self.info = []

        return self.tags

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        soup = bs(raw_report, 'html.parser')
        data = self.parse(soup)
        for item in data:
            event = self.new_event(report)
            event.add('time.source', parser.parse(item[0]).isoformat() + "UTC")
            event.add('source.fqdn', item[1], raise_failure=False)
            event.add('source.ip', item[1], raise_failure=False)
            event.add('source.url', item[3])
            event.add('malware.hash.md5', item[4])
            event.add('classification.type', 'c&c')
            event.add('raw', item[5])
            self.send_message(event)
        self.acknowledge_message()


BOT = CybercrimeParserBot
