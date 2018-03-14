# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.honeydb.parser import \
    HoneydbParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'test_parser_honeydb.json')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "Honeydb feed",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2018-03-10T12:01:48+00:00"
                  }
EXAMPLE_EVENT = {
    "__type": "Event",
    "feed.name": "Honeydb feed",
    "classification.type": "scanner",
    "raw": "eyJjb3VudCI6ICIxMzIwMDAiLCAibGFzdF9zZWVuIjogIjIwMTgtMDMtMTAiLCAicmVtb3RlX2hvc3QiOiAiMTYzLjE3Mi4xOTguMjQ2In0=",
    "time.observation": "2015-09-02T14:17:58+00:00",
    "time.source": "2018-03-10T00:00:00+00:00",
    "source.ip": "163.172.198.246"
    }


class TestHoneydbParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HoneydbParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HoneydbParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
