# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.aa419.parser import Aa419ParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_aa419.data')) as handle:
    REPORT_DATA = handle.read()


REPORT = {"__type": "Report",
          "feed.name": "fake sites list feed",
          "feed.url": "https://db.aa419.org/fakebankslist.php",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-03-03T11:25:09+00:00"
          }
EVENT1 = {"feed.url": "https://db.aa419.org/fakebankslist.php",
          "time.observation": "2018-03-03T11:25:09+00:00",
          "raw": "PHRkPjxhIGhyZWY9Imh0dHA6Ly93d3cuY29hc3RhbG9pbGdhc2NvcnAuY29tIiByZWw9Im5vZm9sbG93IiB0YXJnZXQ9Il9ibGF"
                 "uayI+aHR0cDovL3d3dy5jb2FzdGFsb2lsZ2FzY29ycC5jb208L2E+wqA8L3RkPjx0ZD5Db2FzdGFsIE9pbCAmYW1wOyBHYXMgQ2"
                 "9ycC7CoDwvdGQ+PHRkIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2JhKDI1NSwwLDAsMC4xNSk7Ij5hY3RpdmXCoDwvdGQ+PH"
                 "RkPjIwMTgtMDMtMDMgMDk6NDfCoDwvdGQ+PHRkPjIwMTgtMDMtMDMgMDk6NDfCoDwvdGQ+",
          "feed.name": "fake sites list feed",
          "extra.last_updated": "2018-03-03 09:47",
          "extra.phishing_site": "Coastal Oil & Gas Corp.",
          "extra.phishing_status": "active",
          "source.url": "http://www.coastaloilgascorp.com",
          "classification.type": "phishing",
          "time.source": "2018-03-03T09:47:00+00:00",
          "__type": "Event"}
EVENT2 = {"__type": "Event",
          "feed.name": "fake sites list feed",
          "extra.last_updated": "2018-03-03 08:55",
          "extra.phishing_site": "VP Investment Bank",
          "extra.phishing_status": "active",
          "raw": "PHRkPjxhIGhyZWY9Imh0dHA6Ly93d3cudnByaXZhdGVvbmxpbmUuY29tIiByZWw9Im5vZm9sbG93IiB0YXJnZXQ9Il9ibG"
                 "FuayI+aHR0cDovL3d3dy52cHJpdmF0ZW9ubGluZS5jb208L2E+wqA8L3RkPjx0ZD5WUCBJbnZlc3RtZW50IEJhbmvCoDwvd"
                 "GQ+PHRkIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2JhKDI1NSwwLDAsMC4xNSk7Ij5hY3RpdmXCoDwvdGQ+PHRkPjIwM"
                 "TgtMDMtMDMgMDg6NTXCoDwvdGQ+PHRkPjIwMTgtMDMtMDMgMDg6NTXCoDwvdGQ+",
          "time.observation": "2018-03-03T11:25:09+00:00",
          "time.source": "2018-03-03T08:55:00+00:00",
          "classification.type": "phishing",
          "source.url": "http://www.vprivateonline.com",
          "feed.url": "https://db.aa419.org/fakebankslist.php"}


class TestAa419ParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = Aa419ParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)


if __name__ == '__main__':
    unittest.main()
