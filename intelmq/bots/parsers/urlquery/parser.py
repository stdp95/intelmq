# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from dateutil import parser

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class UrlQueryParserBot(ParserBot):
    def init(self):
        self.tags = []
        self.raw = ''
        self.info = []
        self.collectfeeddata =False
        self.collectfeedurl = []

    def parse(self, soup):
        for td in soup.findAll('td'):
            if td.text != " " and td.text != "":
                if td.text == 'Referer:':
                    self.collectfeeddata = True
                    continue
                if self.collectfeeddata:
                    self.info.append(td.text)
                    self.raw += '%s' % (td)
                    if td.find('a') is not None:
                        self.collectfeedurl.append([td.find('a')['title']])
                    if len(self.info) % 4 == 0:
                        self.tags.append(self.info)
                        self.tags[len(self.tags) - 1].append(self.raw)
                        self.raw = ''
                        self.info = []

        return self.collectfeedurl, self.tags

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        soup = bs(raw_report, 'html.parser')
        urls,data = self.parse(soup)
        for i,item in enumerate(data):
            event = self.new_event(report)
            event.add('time.source', parser.parse(item[0]).isoformat() + "UTC")
            event.add('source.url', urls[i], raise_failure=False)
            event.add('source.ip', item[3])
            event.add('classification.type', 'malware')
            event.add('raw', item[4])
            self.send_message(event)
        self.acknowledge_message()


BOT = UrlQueryParserBot
