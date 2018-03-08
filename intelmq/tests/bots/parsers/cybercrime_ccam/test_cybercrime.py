# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.cybercrime_ccam.parser import CybercrimeParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_cybercrime.data'), 'rb') as handle:
    REPORT_DATA = handle.read()


REPORT = {"__type": "Report",
          "feed.name": "cyber crime Feed",
          "feed.url": "https://cybercrime-tracker.net/ccam.php",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-03-01T10:38:29+00:00"
          }
EVENT1 = {"feed.url": "https://cybercrime-tracker.net/ccam.php",
          "time.observation": "2018-03-01T10:38:29+00:00",
          "raw": "PHRkIGFsaWduPSJjZW50ZXIiIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMTEsIDExLCAxMSk7Ij5UYXl1e"
                 "WE8L3RkPjx0ZCBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiKDExLCAxMSwgMTEpOyI+MjAvMDEvMjAxOCAxMD"
                 "oyMTo1NDwvdGQ+PHRkIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMTEsIDExLCAxMSk7Ij4xOTMuMC4xNzgu"
                 "MTg8L3RkPjx0ZCBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiKDExLCAxMSwgMTEpOyI+PGEgY2xhc3M9Im9sZC"
                 "IgaHJlZj0iY2NhbWRldGFpbC5waHA/aGFzaD0zYzQ5NmVmYTZjNzM1YTZiNjg1M2Y3MTljNjdiMzY5MWI5MDQ4NDZiI"
                 "iB0aXRsZT0iREVUQUlMUyI+M2M0OTZlZmE2YzczNWE2YjY4NTNmNzE5YzY3YjM2OTFiOTA0ODQ2YjwvYT48L3RkPg==",
          "source.ip": "193.0.178.18",
          "malware.hash.md5": "3c496efa6c735a6b6853f719c67b3691b904846b",
          "malware.name": "tayuya",
          "feed.name": "cyber crime Feed",
          "classification.type": "malware",
          "time.source": "2018-01-20T10:21:54+00:00",
          "__type": "Event"}
EVENT2 = {"__type": "Event",
          "feed.name": "cyber crime Feed",
          "raw": "PHRkIGFsaWduPSJjZW50ZXIiIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMTEsIDExLCAxMSk7Ij5UYXl1eWE8L"
                 "3RkPjx0ZCBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogcmdiKDExLCAxMSwgMTEpOyI+MjAvMDEvMjAxOCAxMDoxODowMz"
                 "wvdGQ+PHRkIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiByZ2IoMTEsIDExLCAxMSk7Ij4xNTQuMTYuMTM4Ljg2PC90ZD48"
                 "dGQgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6IHJnYigxMSwgMTEsIDExKTsiPjxhIGNsYXNzPSJvbGQiIGhyZWY9ImNjYW1"
                 "kZXRhaWwucGhwP2hhc2g9N2NmNTQ1N2ExMGJlOTQ0ZTk0M2NhNGJhZDBjNzk5ZTE0ZjRiNzE3ZiIgdGl0bGU9IkRFVEFJTFM"
                 "iPjdjZjU0NTdhMTBiZTk0NGU5NDNjYTRiYWQwYzc5OWUxNGY0YjcxN2Y8L2E+PC90ZD4=",
          "time.observation": "2018-03-01T10:38:29+00:00",
          "malware.hash.md5": "7cf5457a10be944e943ca4bad0c799e14f4b717f",
          "malware.name": "tayuya",
          "time.source": "2018-01-20T10:18:03+00:00",
          "classification.type": "malware",
          "feed.url": "https://cybercrime-tracker.net/ccam.php",
          "source.ip": "154.16.138.86"}


class TestCybercrimeParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CybercrimeParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)


if __name__ == '__main__':
    unittest.main()
