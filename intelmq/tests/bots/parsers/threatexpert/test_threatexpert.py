# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.threatexpert.parser import ThreatExpertParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_threatexpert.data')) as handle:
    REPORT_DATA = handle.read()


REPORT = {"__type": "Report",
          "feed.name": "Threat expert Feed",
          "feed.url": "http://www.threatexpert.com/reports.aspx?tf=2&sl=1",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-03-21T09:53:32+00:00"
          }
EVENT1 = {"feed.url": "http://www.threatexpert.com/reports.aspx?tf=2&sl=1",
          "time.observation": "2018-03-21T09:53:32+00:00",
          "raw": "PHRkIHdpZHRoPSIxNTBweCI+My8xNy8yMDE4IDI6MDk6MDAgQU08L3RkPjx0ZD48YSBocmVmPSJyZXBvcnQuY"
                 "XNweD9tZDU9MzFhMjRiMDJjNjNhODhiYjgzNjY1Y2RiYmEzNGM1ODQiIHRhcmdldD0iX2JsYW5rIj48Zm9udCB"
                 "jb2xvcj0iI2EwMDAwMCI+QmFja2Rvb3IuV2luMzIuRmx5QWdlbnQsIFRyb2phbkRvd25sb2FkZXI6V2luMzIvU21hb"
                 "GwuZ2VuIUM8L2ZvbnQ+PC9hPjwvdGQ+",
          "feed.name": "Threat expert Feed",
          "classification.type": "malware",
          "malware.name": "backdoor.win32.flyagent",
          "malware.hash.md5": "31a24b02c63a88bb83665cdbba34c584",
          "time.source": "2018-03-17T02:09:00+00:00",
          "__type": "Event"}
EVENT2 = {"__type": "Event",
          "feed.name": "Threat expert Feed",
          "raw": "PHRkIHdpZHRoPSIxNTBweCI+My8xNy8yMDE4IDI6MDk6MDAgQU08L3RkPjx0ZD48YSBocmVmPSJyZXBvcnQuYXNweD9"
                 "tZDU9MzFhMjRiMDJjNjNhODhiYjgzNjY1Y2RiYmEzNGM1ODQiIHRhcmdldD0iX2JsYW5rIj48Zm9udCBjb2xvcj0iI2EwMD"
                 "AwMCI+QmFja2Rvb3IuV2luMzIuRmx5QWdlbnQsIFRyb2phbkRvd25sb2FkZXI6V2luMzIvU21hbGwuZ2VuIUM8L2ZvbnQ+PC9hPjwvdGQ+",
          "time.observation": "2018-03-01T10:38:29+00:00",
          "malware.hash.md5": "31a24b02c63a88bb83665cdbba34c584",
          "time.source": "2018-03-17T02:09:00+00:00",
          "malware.name": "trojandownloader:win32/small.gen!c",
          "classification.type": "malware",
          "feed.url": "http://www.threatexpert.com/reports.aspx?tf=2&sl=1"}


class TestThreatExpertParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ThreatExpertParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)


if __name__ == '__main__':
    unittest.main()
