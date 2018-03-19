# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.urlquery.parser import UrlQueryParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_urlquery.data')) as handle:
    REPORT_DATA = handle.read()


REPORT = {"__type": "Report",
          "feed.name": "url Query Feed",
          "feed.url": "https://urlquery.net/",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-03-17T06:19:11+00:00"
          }
EVENT1 = {"feed.url": "https://urlquery.net/",
          "time.observation": "2018-03-17T06:19:11+00:00",
          "raw": "PHRkPjxub2JyPjxjZW50ZXI+MjAxOC0wMy0xNiAxNjoxNToxNiBDRVQ8L2NlbnRlcj48L25vYnI+PC90ZD48dGQ"
                 "gYWxpZ249ImNlbnRlciI+PGI+MCAtIDAgLSAwPC9iPjwvdGQ+PHRkPjxhIGhyZWY9InJlcG9ydC9iMWIxZDUyZi"
                 "1kNGI0LTQzNDUtOTk0OC02OGJlNDBhZWRlMDciIHRpdGxlPSJiaXQuZG8vZjI5M2U3NTJmIj5iaXQuZG8vZjI5M"
                 "2U3NTJmPC9hPjwvdGQ+PHRkIHN0eWxlPSJ0ZXh0LWFsaWduOmNlbnRlcjt2ZXJ0aWNhbC1hbGlnbj1taWRkbGU7I"
                 "j48aW1nIGFsaWduPSJsZWZ0IiBoZWlnaHQ9IjExIiBzcmM9Ii9zdGF0aWMvb3JnL2ltYWdlcy9mbGFncy91cy5wb"
                 "mciIHRpdGxlPSJVbml0ZWQgU3RhdGVzIiB3aWR0aD0iMTYiLz41NC44My41Mi43NjwvdGQ+",
          "source.ip": "54.83.52.76",
          "feed.name": "url Query Feed",
          "classification.type": "malware",
          "time.source": "2018-03-16T16:15:16+00:00",
          "__type": "Event"}
EVENT2 = {"__type": "Event",
          "feed.name": "url Query Feed",
          "raw": "PHRkPjxub2JyPjxjZW50ZXI+MjAxOC0wMy0xNiAxNjoxNToxNSBDRVQ8L2NlbnRlcj48L25vYnI+PC90ZD48dGQgYWx"
                 "pZ249ImNlbnRlciI+PGI+MCAtIDAgLSAwPC9iPjwvdGQ+PHRkPjxhIGhyZWY9InJlcG9ydC9kNDQyMjRkYy1kMTdlLTQ"
                 "zMGYtYWJhOS04ODk1ZDU3Y2EwNWEiIHRpdGxlPSJodHRwczovL3N1cnZleS5xdWFsdHJpY3MuY29tL2oiPmh0dHBzOi8"
                 "vc3VydmV5LnF1YWx0cmljcy5jb20vajwvYT48L3RkPjx0ZCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7dmVydGljYWwt"
                 "YWxpZ249bWlkZGxlOyI+PGltZyBhbGlnbj0ibGVmdCIgaGVpZ2h0PSIxMSIgc3JjPSIvc3RhdGljL29yZy9pbWFnZXMv"
                 "ZmxhZ3MvdXMucG5nIiB0aXRsZT0iVW5pdGVkIFN0YXRlcyIgd2lkdGg9IjE2Ii8+MTA0LjEyMy4xMzYuMTQ3PC90ZD4=",
          "time.observation": "2018-03-17T06:19:11+00:00",
          "time.source": "2018-03-16T16:15:15+00:00",
          "classification.type": "malware",
          "feed.url": "https://urlquery.net/",
          "source.ip": "104.123.136.147"}


class TestUrlQueryParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = UrlQueryParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)


if __name__ == '__main__':
    unittest.main()
