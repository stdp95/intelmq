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
        for td in soup.findAll('td'):
            self.info.append(td.text)
            self.raw += '%s'%(td)
            if len(self.info)%5 == 0:
                self.info.pop(-1)
                self.tags.append(self.info)
                self.tags[len(self.tags)-1].append(self.raw)
                self.raw = ''
                self.info = []
        return self.tags

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        soup = bs(raw_report, 'html.parser')
        data = self.parse(soup)
        data.pop(0)
        for item in data:
            event = self.new_event(report)
            event.add('malware.name', item[3])
            event.add('time.source', parser.parse(item[0]).isoformat()+"UTC")
            if not item[1].startswith("http"): item[1] = "http://"+item[1]
            event.add('source.url', item[1])
            event.add('source.ip', item[2], raise_failure=False)
            event.add('classification.type', 'malware')
            event.add('raw', item[4])
            self.send_message(event)
        self.acknowledge_message()


BOT = CybercrimeParserBot
