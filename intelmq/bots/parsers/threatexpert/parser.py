# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from dateutil import parser

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot



class ThreatExpertParserBot(ParserBot):
    def init(self):
        self.feed = []
        self.raw = ''
        self.values = []
        self.collectfeeddata = False

    def parse(self, soup):
        for td in soup.findAll('td'):
            if td.text != " " and td.text != "" :
                if td.text =="Findings":
                    self.collectfeeddata = True
                    continue
                if self.collectfeeddata:
                    if td.attrs=={'width': '150px'}:
                        self.values.append(td.text)
                        self.raw += '%s'%(td)
                    if td.find('a') is not None and len(td.find('a')['href'].split('report.aspx?md5='))!=1:
                        self.values.append(td.find('a')['href'].split('report.aspx?md5=')[1])
                        self.values.append(td.text)
                        self.raw += '%s'%(td)
                        if len(self.values)%3 == 0:
                            self.feed.append(self.values)
                            self.feed[len(self.feed)-1].append(self.raw)
                            self.raw = ''
                            self.values = []

        return self.feed

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        soup = bs(raw_report, 'html.parser')
        data = self.parse(soup)
        for item in data:
            event = self.new_event(report)
            event.add('time.source',parser.parse(item[0]).isoformat() + "UTC")
            event.add('malware.hash.md5', item[1])
            event.add('classification.type', 'malware')
            event.add('raw', item[3])
            for each_type in item[2].split(','):
                event.add('malware.name',each_type,overwrite=True)
                self.send_message(event)
        self.acknowledge_message()


BOT = ThreatExpertParserBot
