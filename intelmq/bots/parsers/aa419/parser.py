# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot



class Aa419ParserBot(ParserBot):
    def init(self):
        self.tags = []
        self.raw = ''
        self.info = []

    def parse(self, soup):
        for td in soup.findAll('td'):
            if td.text != "" :
                if td.text.endswith('\xa0'): filtered_data = td.text[:-len('\xa0')]
                self.info.append(filtered_data)
                self.raw += '%s'%(td)
                if len(self.info)%5 == 0:
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
        for item in data:
            event = self.new_event(report)
            event.add('source.url', item[0])
            event.add('extra', {"phishing_site":item[1], "phishing_status":item[2], "last_updated":item[4]})
            event.add('time.source', item[3] + "UTC")
            event.add('classification.type', 'phishing')
            event.add('raw', item[5])
            self.send_message(event)
        self.acknowledge_message()


BOT = Aa419ParserBot
