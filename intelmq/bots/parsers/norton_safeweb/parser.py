# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class NortonSafewebParserBot(Bot):

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        soup = bs(raw_report, 'html.parser')
        feed_div = soup.find(id='lthreat')
        feed_list = feed_div.find_all('a')

        for feed in feed_list:
            link = (feed.get('href')).split('name=')[1]

            event = self.new_event(report)
            event.add('classification.type', 'malware')
            event.add('source.ip', link, raise_failure=False)
            if 'source.ip' not in event:
                event.add('source.url', 'http://' + link)
            event.add('raw', feed)
            self.send_message(event)

        self.acknowledge_message()


BOT = NortonSafewebParserBot
