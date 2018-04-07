# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from dateutil import parser

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class MalekalParserBot(ParserBot):
    def init(self):
        self.data = []
        self.raw = ''
        self.feed = []
        self.hash = []

    def parse(self, soup):

        for td in soup.findAll('td'):
            if td.text != " ":
                if td.attrs == {'align': 'center', 'nowrap': ''}:
                    if len(td.text.split('File detection : ')) == 2:
                        self.data.append(td.text.split('File detection : ')[1].split('(')[0])
                        self.raw += '%s' % (td)
                    if len(td.text.split(',')) == 2:
                        self.data.append(td.text.split(',')[1])
                        self.raw += '%s' % (td)
                if td.attrs == {'align': 'left'}:
                    if td.text != "":
                        self.data.append(str(td).split('<td align="left">')[1].split('<br/>')[0])
                        self.raw += '%s' % (td)
                    else:
                        self.data.append(td.text)
                        self.raw += '%s' % (td)
                for a in (td.childGenerator()):
                    if len(str(a).split('hash')) == 2:
                        self.hash.append(str(a).split('hash=')[1].split('"')[0])
                        if len(self.hash) % 3 == 0:
                            self.data.append(self.hash)
                            hash = []
                            self.raw += '%s' % (td)
                if td.attrs == {'align': 'center'}:
                    self.data.append(td.text)
                    self.raw += '%s' % (td)
                    if len(self.data) % 6 == 0:
                        self.feed.append(self.data)
                        self.feed[len(self.feed) - 1].append(self.raw)
                        self.raw = ''
                        self.data = []
        return self.feed

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        soup = bs(raw_report, 'html5lib')
        data = self.parse(soup)
        for item in data:
            event = self.new_event(report)
            event.add('time.source', parser.parse(item[0]).isoformat() + "UTC")
            event.add('malware.hash.md5', item[1][0])
            event.add('malware.hash.sha1', item[1][1])
            event.add('malware.hash.sha256', item[1][2])
            event.add('extra', {'size': item[2]})
            event.add('malware.name', item[3])
            event.add('extra', {'rate': item[4]})
            event.add('classification.type', 'malware')
            event.add('raw', item[6])
            self.send_message(event)
        self.acknowledge_message()


BOT = MalekalParserBot
