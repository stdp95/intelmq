# -*- coding: utf-8 -*-

import os
import unittest
from collections import OrderedDict

import intelmq.lib.test as test
from intelmq.bots.parsers.ekparser.parser import EkParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'data.json')) as handle:
    EXAMPLE_FILE = handle.read()
   


EXAMPLE_REPORT = {"feed.url": "http://ektracker.com/api/entries/",
                  "feed.name": "ek feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "time.observation": "2015-11-02T13:11:43+00:00"
                  }

EXAMPLE_EVENT = {"time.observation": "2015-11-02T13:11:44+00:00",
                   "classification.type": "malware",
                   "classification.taxonomy": "malacious code",
                   "feed.url": "http://ektracker.com/api/entries/",
                   "extra": "{\"tags\": [\"rig\", \"seamless\"]}",
                   "time.source": "2018-01-20T10:35:47+00:00",
                   "source.ip": "176.57.208.50",
                   "feed.name": "ek feed",               "raw":"eyJ0YWdzIjogWyJyaWciLCAic2VhbWxlc3MiXSwgInVybCI6ICIxNzZbLl01N1suXTIwOFsuXTUwIiwgInRpbWVzdGFtcCI6ICIyMDE4LTAxLTIwVDEwOjM1OjQ3IiwgImVudHJ5X2lkIjogMzQ2MCwgInVzZXIiOiAiY3liZXJfYXR0YWNrcyIsICJyZWZlcmVuY2VzIjogW119",
		   "__type": "Event"
                  }


class TestEkParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for EkParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = EkParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        
        self.assertMessageEqual(0, EXAMPLE_EVENT)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
