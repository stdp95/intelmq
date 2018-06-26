# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.norton_safeweb.parser import NortonSafewebParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_norton_safeweb.data')) as handle:
    REPORT_DATA = handle.read()

REPORT = {"__type": "Report",
          "feed.name": "Norton Safeweb Feed",
          "feed.url": "https://safeweb.norton.com/buzz",
          "feed.provider": "safeweb.norton.com",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-05-12T11:16:46+00:00"
          }

EVENT1 = {"feed.name": "Norton Safeweb Feed",
          "feed.url": "https://safeweb.norton.com/buzz",
          "feed.provider": "safeweb.norton.com",
          "source.url": "http://businessweekly.co.bw",
          "time.observation": "2018-05-04T11:16:46+00:00",
          "__type": "Event",
          "classification.type": "malware",
          "raw": "PGEgaHJlZj0iL3JlcG9ydC9zaG93X21vYmlsZT9uYW1lPWJ1c2luZXNzd2Vla2x5LmNvLmJ3IiB0aXRsZT0iVm"
                 "lldyByZXBvcnQgZm9yIGJ1c2luZXNzd2Vla2x5LmNvLmJ3Ij5idXNpbmVzc3dlZWtseS4uLi48L2E+"
          }


class TestNortonSafewebParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = NortonSafewebParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)


if __name__ == '__main__':
    unittest.main
