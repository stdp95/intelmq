# -*- coding: utf-8 -*-
""" Parser for urandom.us.to feeds. """

from dateutil.parser import parse

from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event


class UrandomParserBot(ParserBot):
    """ Parser for urandom.us.to feed. """

    def parse_line(self, line, report):
        if line.startswith('#') or 'IP=' not in line or not line.startswith('['):
            self.tempdata.append(line)
        else:
            date_start = 1
            date_end = line.find(']')
            date = parse(line[date_start:date_end], fuzzy=True).isoformat() + " UTC"

            start = 0
            tagslist = []
            while True:
                token_end = line[start:].find('=')
                if token_end < 0:
                    break
                token_start = line[start:start + token_end].rfind(' ')
                token = line[start + token_start:start + token_end + 1]
                tagslist.append({'tag': token[1:-1],
                                'start': start + token_start,
                                 'end': start + token_end + 1})
                start = start + token_end + 1
            tagslist.append({'tag': None, 'start': len(line), 'end': len(line)})

            last_tag = None
            last_tgend = 0
            tgvals = {}
            for tag in tagslist:
                if not last_tag:
                    last_tgend = tag['end']
                    last_tag = tag['tag']
                else:
                    tgstart = tag['start']
                    tgvals[last_tag] = line[last_tgend:tgstart]
                    last_tgend = tag['end']
                    last_tag = tag['tag']

            event = Event(report)
            extra = {}
            event.add('time.source', date)
            if 'IP' in tgvals:
                    event.add('source.ip', tgvals['IP'])
            if 'TAG' in tgvals:
                    extra['tags'] = tgvals['TAG']
            if 'SOURCE' in tgvals:
                    extra['source'] = tgvals['SOURCE']
            event.add('classification.type', 'scanner')
            event.add('raw', line)

            yield event


BOT = UrandomParserBot
