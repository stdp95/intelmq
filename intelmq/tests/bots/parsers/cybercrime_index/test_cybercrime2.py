# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.cybercrime_index.parser import CybercrimeParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_malwareurl.data'), 'rb') as handle:
    REPORT_DATA = handle.read()


REPORT = {"__type": "Report",
          "feed.name": "cyber crime tracker feed",
          "feed.url": "https://cybercrime-tracker.net/index.php",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-03-03T06:20:53+00:00"
          }
EVENT1 = {"feed.url": "https://cybercrime-tracker.net/index.php",
          "time.observation": "2018-03-01T10:38:29+00:00",
          "raw": "PHRkPjAyLTAzLTIwMTg8L3RkPjx0ZD5yZXNvbHV0ZmVwLmNvbS9hbG96aWUvZW5nL2FkbWluLnBocDwvdGQ+PHRkPjxhIGhyZWY9Imh0dHBz"
                 "Oi8vd3d3LnZpcnVzdG90YWwuY29tL2VuL2lwLWFkZHJlc3MvMTAzLjczLjE5MC4yMzQvaW5mb3JtYXRpb24vIiB0YXJnZXQ9Il9ibGFuayI+M"
                 "TAzLjczLjE5MC4yMzQ8L2E+PC90ZD48dGQ+UG9ueTwvdGQ+PHRkPjxhIGhyZWY9Imh0dHBzOi8vd3d3LnZpcnVzdG90YWwuY29tL2xhdGVzdC"
                 "1zY2FuL2h0dHA6Ly9yZXNvbHV0ZmVwLmNvbS9hbG96aWUvZW5nL2FkbWluLnBocCIgdGFyZ2V0PSJfYmxhbmsiPjxpbWcgYm9yZGVyPSIwIiB"
                 "oZWlnaHQ9IjEyIiBzcmM9InZ0LnBuZyIgdGl0bGU9IlNjYW4gd2l0aCBWaXJ1c1RvdGFsIiB3aWR0aD0iMTMiLz48L2E+IDxhIGhyZWY9Imh0"
                 "dHA6Ly9jeWJlcmNyaW1lLXRyYWNrZXIubmV0L2luZGV4LnBocD9zPTAmYW1wO209NDAmYW1wO3NlYXJjaD1Qb255Ij48aW1nIGJvcmRlcj0iM"
                 "CIgaGVpZ2h0PSIxMiIgc3JjPSJ2d2ljbjAwOC5naWYiIHRpdGxlPSJTZWFyY2ggdGhlIGZhbWlseSIgd2lkdGg9IjEzIi8+PC9hPjwvdGQ+",
          "source.ip": "103.73.190.234",
          "source.url": "http://resolutfep.com/alozie/eng/admin.php",
          "malware.name": "pony",
          "feed.name": "cyber crime tracker feed",
          "classification.type": "malware",
          "time.source": "2018-02-03T00:00:00+00:00",
          "__type": "Event"}
EVENT2 = {"__type": "Event",
          "feed.name": "cyber crime tracker feed",
          "raw": "PHRkPjAyLTAzLTIwMTg8L3RkPjx0ZD5jYXBvbnBlbGxhbWkuY29tL2xhdy9kaW8vYWRtaW4ucGhwPC90ZD48dGQ+PGEgaHJlZj0iaHR0cHM6"
                 "Ly93d3cudmlydXN0b3RhbC5jb20vZW4vaXAtYWRkcmVzcy8xMDMuNzMuMTkwLjIzNC9pbmZvcm1hdGlvbi8iIHRhcmdldD0iX2JsYW5rIj4x"
                 "MDMuNzMuMTkwLjIzNDwvYT48L3RkPjx0ZD5Qb255PC90ZD48dGQ+PGEgaHJlZj0iaHR0cHM6Ly93d3cudmlydXN0b3RhbC5jb20vbGF0ZXN0"
                 "LXNjYW4vaHR0cDovL2NhcG9ucGVsbGFtaS5jb20vbGF3L2Rpby9hZG1pbi5waHAiIHRhcmdldD0iX2JsYW5rIj48aW1nIGJvcmRlcj0iMCIg"
                 "aGVpZ2h0PSIxMiIgc3JjPSJ2dC5wbmciIHRpdGxlPSJTY2FuIHdpdGggVmlydXNUb3RhbCIgd2lkdGg9IjEzIi8+PC9hPiA8YSBocmVmPSJo"
                 "dHRwOi8vY3liZXJjcmltZS10cmFja2VyLm5ldC9pbmRleC5waHA/cz0wJmFtcDttPTQwJmFtcDtzZWFyY2g9UG9ueSI+PGltZyBib3JkZXI9"
                 "IjAiIGhlaWdodD0iMTIiIHNyYz0idndpY24wMDguZ2lmIiB0aXRsZT0iU2VhcmNoIHRoZSBmYW1pbHkiIHdpZHRoPSIxMyIvPjwvYT48L3RkPg==",
          "time.observation": "2018-03-01T10:38:29+00:00",
          "malware.name": "pony",
          "time.source": "2018-02-03T00:00:00+00:00",
          "classification.type": "malware",
          "source.url": "http://caponpellami.com/law/dio/admin.php",
          "feed.url": "https://cybercrime-tracker.net/index.php",
          "source.ip": "103.73.190.234"}


class TestCybercrimeParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CybercrimeParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)


if __name__ == '__main__':
    unittest.main()
