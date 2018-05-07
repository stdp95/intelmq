# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.talos.parser import TalosParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'data.json')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.url": "https://www.talosintelligence.com/sb_api/query_lookup?query=%2Fapi%2Fv2%2F"
                              "top_stats%2Ftop_senders&query_entry%5Bduration%5D=lastday&query_entry%5Blimit"
                              "%5D=100&query_entry%5Bsender_type%5D=virus",
                  "feed.name": "Talos Feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "time.observation": "2018-05-07T10:06:14+00:00"
                  }

EXAMPLE_EVENT = {"time.observation": "2015-11-02T13:11:44+00:00",
                 "classification.type": "malware",
                 "feed.url": "https://www.talosintelligence.com/sb_api/query_lookup?query=%2Fapi%2Fv2%2Ft"
                             "op_stats%2Ftop_senders&query_entry%5Bduration%5D=lastday&query_entry%5Blimit"
                             "%5D=100&query_entry%5Bsender_type%5D=virus",
                 "source.ip": "172.93.98.60",
                 "feed.name": "Talos Feed",
                 "source.fqdn": "hosted-by.sneakygorilla.com",
                 "raw": "eyJpcCI6ICIxNzIuOTMuOTguNjAiLCAiaG9zdG5hbWUiOiAiaG9zdGVkLWJ5LnNuZWFreWdvcmlsbGEuY29tIi"
                        "wgInZvbHVtZV9jaGFuZ2UiOiAyNTAwLjAsICJsb25naXR1ZGUiOiAtNzMuOTc4MiwgInZvbHVtZSI6IDUuMzM3M"
                        "zMsICJjb3VudHJ5X25hbWUiOiAiVW5pdGVkIFN0YXRlcyIsICJmbGFnIjogIi9pbWFnZXMvZmxhZ3MvVVMucG5nI"
                        "iwgInJlcHV0YXRpb24iOiAiIiwgImlwX2ludCI6IDI4OTE4MDExNDgsICJsYXRpdHVkZSI6IDQwLjc0NDksICJvcm"
                        "dhbml6YXRpb24iOiAiUmVsaWFibGVTaXRlLk5ldCBMTEMiLCAiY291bnRyeSI6ICJVUyJ9",
                 "__type": "Event"
                 }


class TestTalosParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TalosParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TalosParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
