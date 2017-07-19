# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.urandom.parser import UrandomParserBot

with open(os.path.join(os.path.dirname(__file__), 'vnc.txt')) as handle:
    VNC_FILE = handle.read()

VNC_REPORT = {'feed.name': 'Urandom VNC attacker IPs',
                'feed.url': 'http://urandom.us.to/report.php?ip=&info=&tag=vnc&out=csv&submit=go',
                '__type': 'Report',
                'time.observation': '2017-07-11T00:00:00+00:00',
                'raw': utils.base64_encode(VNC_FILE)
               }

VNC_EVENTS = [{'feed.name': 'Urandom VNC attacker IPs',
                 'feed.url': 'http://urandom.us.to/report.php?ip=&info=&tag=vnc&out=csv&submit=go',
                 '__type': 'Event',
                 'time.observation': '2017-07-11T00:00:00+00:00',
                 'raw': 'W0p1bCAxMSAyMDE3XSBJUD0xNzMuMTg0LjE5MC4yMDQgSU5GTz0oQVM3MDI5IFdJTkRTVFJFQU0tQUdHKSBUQUc9dm5jIFNPVVJDRT1hdG1hLmVz',
                 'time.source': '2017-07-11T00:00:00+00:00',
                 'source.ip': '173.184.190.204',
                 'classification.type': 'scanner',
                },
                {'feed.name': 'Urandom VNC attacker IPs',
                 'feed.url': 'http://urandom.us.to/report.php?ip=&info=&tag=vnc&out=csv&submit=go',
                 '__type': 'Event',
                 'time.observation': '2016-12-04T07:50:15+00:00',
                 'raw': 'W0p1bCAxMSAyMDE3XSBJUD0xNjkuMTM5LjU2LjIxOCBJTkZPPShCUk9XLUsxMi1GTCBVUykgVEFHPXZuYyBTT1VSQ0U9YXRtYS5lcw==',
                 'time.source': '2017-07-11T00:00:00+00:00',
                 'source.ip': '169.139.56.218',
                 'classification.type': 'scanner',
                }]

class TestUrandomParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = UrandomParserBot
        cls.default_input_message = VNC_REPORT

    def test_hosts(self):
        """ Test if correct Events have been produced. """
        self.run_bot()
        self.assertMessageEqual(0, VNC_EVENTS[0])
        self.assertMessageEqual(1, VNC_EVENTS[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
