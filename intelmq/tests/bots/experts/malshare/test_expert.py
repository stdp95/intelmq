# -*- coding: utf-8 -*-
"""
Testing MalShareExpertBot.
"""

import unittest
import json

from pkg_resources import resource_filename

import intelmq.lib.test as test
from intelmq.lib.utils import load_configuration
from intelmq.bots.experts.malshare.expert import MalShareExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "feed.accuracy": 100,
                 "feed.name": "MalShare Feed",
                 "feed.provider": "malshare.com",
                 "feed.url": "https://malshare.com/daily/malshare.current.txt",
                 "time.observation": "2018-04-25T13:34:28+00:00",
                 "malware.hash.md5": "56758ced477d2a615939c2fb29c63833"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "feed.accuracy": 100,
                  "feed.name": "MalShare Feed",
                  "feed.provider": "malshare.com",
                  "feed.url": "https://malshare.com/daily/malshare.current.txt",
                  "time.observation": "2018-04-25T13:34:28+00:00",
                  "malware.hash.md5": "56758ced477d2a615939c2fb29c63833",
                  "malware.hash.sha1": "c80c09672fe3df7c035dfa713d339d091ee7fc97",
                  "malware.hash.sha256": "60879c83b942fbc8d63d7811a718b26eaef7c7c6174653e44fce94fffc1ffa07",
                  "source.url": "http://bittabi.net/z0IvVB/index.html"
                  }


class TestMalShareExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for MalShareExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MalShareExpertBot
        # Configuring path to  the api key stored at parser directory in default.json file
        config_path = resource_filename('intelmq', 'bots/experts/malshare/default.json')
        api = json.loads(open(config_path).read())
        cls.sysconfig = {'api_key': key[0]["api_key"]}

    def test_event(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
