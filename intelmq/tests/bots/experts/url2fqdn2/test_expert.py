# -*- coding: utf-8 -*-
"""
Testing url2fqdn.
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.url2fqdn2.expert import Url2fqdnExpertBot

EXAMPLE_INPUT_1 = {"__type": "Event",
                   "source.url": "http://example.com/something/index.php",
                   "destination.url": "http://example.org/download?file.exe",
                   "time.observation": "2015-01-01T00:00:00+00:00"}
EXAMPLE_INPUT_2 = {"__type": "Event",
                   "source.url": "http://10.0.0.0/something/index.php",
                   "destination.url": "http://example.org/download?file.exe",
                   "time.observation": "2015-01-01T00:00:00+00:00"}
EXAMPLE_OUTPUT_1 = {"__type": "Event",
                    "source.url": "http://example.com/something/index.php",
                    "destination.url": "http://example.org/download?file.exe",
                    "source.fqdn": "example.com",
                    "destination.fqdn": "example.org",
                    "time.observation": "2015-01-01T00:00:00+00:00",
                    "source.urlpath": "/something/index.php",
                    "destination.urlpath": "/download"}

EXAMPLE_OUTPUT_2 = {"__type": "Event",
                    "source.url": "http://10.0.0.0/something/index.php",
                    "destination.url": "http://example.org/download?file.exe",
                    "source.ip": "10.0.0.0",
                    "destination.fqdn": "example.org",
                    "time.observation": "2015-01-01T00:00:00+00:00",
                    "source.urlpath": "/something/index.php",
                    "destination.urlpath": "/download"}


class TestUrl2fqdnExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Url2fqdnExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = Url2fqdnExpertBot

    def test(self):
        self.input_message = EXAMPLE_INPUT_1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_1)

    def test_event_with_ip(self):
        self.input_message = EXAMPLE_INPUT_2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_2)

    def test_overwrite(self):
        self.input_message = EXAMPLE_INPUT_1.copy()
        self.input_message['source.fqdn'] = 'example.net'
        self.sysconfig = {'overwrite': True}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
