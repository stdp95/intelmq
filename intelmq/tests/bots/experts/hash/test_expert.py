# -*- coding: utf-8 -*-
"""
Testing HashExpertBot.
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.hash.expert import HashExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "feed.accuracy": 100,
                 "feed.name": "Malware Domain List",
                 "feed.provider": "Malware Domain List",
                 "feed.url": "http://www.malwaredomainlist.com/updatescsv.php",
                 "time.observation": "2018-04-25T13:34:28+00:00",
                 "time.source": "2017-05-01T16:22:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "feed.accuracy": 100,
                  "feed.name": "Malware Domain List",
                  "feed.provider": "Malware Domain List",
                  "feed.url": "http://www.malwaredomainlist.com/updatescsv.php",
                  "time.observation": "2018-04-25T13:34:28+00:00",
                  "time.source": "2017-05-01T16:22:00+00:00",
                  "extra.message_hash": "393940ee5f52f8c479cc7d438d1b7265d2e2242402e9dcb31b1f71eb96d0288b"
                  }


class TestHashExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HashExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = HashExpertBot

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
