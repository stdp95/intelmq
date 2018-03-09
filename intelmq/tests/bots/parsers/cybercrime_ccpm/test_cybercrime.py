# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.cybercrime_ccpm.parser import CybercrimeParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_cybercrime.data'), 'rb') as handle:
    REPORT_DATA = handle.read()


REPORT = {"__type": "Report",
          "feed.name": "cyber crime feed",
          "feed.url": "https://cybercrime-tracker.net/ccpm.php",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-03-03T06:20:53+00:00"
          }
EVENT1 = {"feed.url": "https://cybercrime-tracker.net/ccpm.php",
          "time.observation": "2018-03-01T10:38:29+00:00",
          "source.fqdn": "bot.myru.info",
          "raw": "PHRkIGFsaWduPSJNSURETEUiPjA4LzAzLzIwMTggMjM6NTQ6MDA8L3RkPjx0ZCBhbGlnbj0iTUlERExFIj48YSBocmVmP"
                 "SJodHRwczovL3d3dy52aXJ1c3RvdGFsLmNvbS9lbi9kb21haW4vQk9ULk1ZUlUuSU5GTy9pbmZvcm1hdGlvbi8iPkJPVC5"
                 "NWVJVLklORk88L2E+PC90ZD48dGQgYWxpZ249Ik1JRERMRSI+OTg4MTY8L3RkPjx0ZCBhbGlnbj0iTUlERExFIj48YSBoc"
                 "mVmPSJodHRwczovL3d3dy52aXJ1c3RvdGFsLmNvbS91cmwvYWM2MzM2MjFhYWIyYTZmNzc4MDc2ODllNzZjYTdlMzk5ZTg"
                 "3YjBhMTI2MGZmOTdiMWVhYTcyYWY4YmQ4ZThjNi9hbmFseXNpcy8xNTIwNTQ5NjM5LyIgdGl0bGU9IipGUkVTSCoiPmh0dH"
                 "A6Ly9ib3QubXlydS5pbmZvL3BhbmVsL2dhdGUucGhwPC9hPjwvdGQ+PHRkIGFsaWduPSJNSURETEUiPjxhIGhyZWY9Imh0"
                 "dHA6Ly9jeWJlcmNyaW1lLXRyYWNrZXIubmV0L2Rpc3BhdGNoaW5nL2luZGV4LnBocD9kaXI9cG9ueS8mYW1wO2ZpbGU9NWI"
                 "xNWJjNjQxNDU0ZTEzNWU2OTVmMzkzNTM3OGIzYTkwMWMzZTVkZmRkNGRhMTExNDRjM2VmMzY3ZDRiZjc4MyI+MWU0MzAyN2Q"
                 "3MTAwMDk1N2RhNTAzMzczNjc3MmVjMWE8L2E+PC90ZD4=",
          "source.url": "http://bot.myru.info/panel/gate.php",
          "feed.name": "cyber crime feed",
          "malware.hash.md5": "1e43027d71000957da5033736772ec1a",
          "classification.type": "c&c",
          "time.source": "2018-08-03T23:54:00+00:00",
          "__type": "Event"}
EVENT2 = {"__type": "Event",
          "feed.name": "cyber crime feed",
          "time.observation": "2018-03-01T10:38:29+00:00",
          "raw": "PHRkIGFsaWduPSJNSURETEUiPjA4LzAzLzIwMTggMjM6NTI6MDk8L3RkPjx0ZCBhbGlnbj0iTUlERExFIj48YSBocmVmPS"
                 "JodHRwczovL3d3dy52aXJ1c3RvdGFsLmNvbS9lbi9kb21haW4vQVNJR1VSQVJJLURBVU5FLURFU1BBR1VCSVJJLlJPL2lu"
                 "Zm9ybWF0aW9uLyI+QVNJR1VSQVJJLURBVU5FLURFU1BBR1VCSVJJLlJPPC9hPjwvdGQ+PHRkIGFsaWduPSJNSURETEUiPj"
                 "k5MzI4PC90ZD48dGQgYWxpZ249Ik1JRERMRSI+PGEgaHJlZj0iaHR0cHM6Ly93d3cudmlydXN0b3RhbC5jb20vdXJsLzVmO"
                 "DVlYWFlNDMxN2QyYzU2ZjNjNzRhODg2ZjZlZWM2ZjI2YTcwODg0ZmU0ZjU3ZTM1OTU3NjQzNzczZGRkNTIvYW5hbHlzaXMv"
                 "MTUyMDU0OTUyOC8iIHRpdGxlPSIqRlJFU0gqIj5odHRwOi8vYXNpZ3VyYXJpLWRhdW5lLWRlc3BhZ3ViaXJpLnJvL3dwLWR"
                 "hdGFiYXNlL3N0YWlubWFuL2dhdGUucGhwPC9hPjwvdGQ+PHRkIGFsaWduPSJNSURETEUiPjxhIGhyZWY9Imh0dHA6Ly9jeW"
                 "JlcmNyaW1lLXRyYWNrZXIubmV0L2Rpc3BhdGNoaW5nL2luZGV4LnBocD9kaXI9cG9ueS8mYW1wO2ZpbGU9YTg5ZDQ3N2ZlO"
                 "WUzYTY3OTFhMTBiM2E3M2I3YTllNDkxYThkNzE1N2U1YzRmNTQ5NDhjY2RmODE4NDJiMDA3NCI+MjlhZmZjNzk5NmY0YTczN"
                 "jk1NmEwZDg5MDY4NGNkZTc8L2E+PC90ZD4=",
          "time.source": "2018-08-03T23:52:09+00:00",
          "classification.type": "c&c",
          "feed.url": "https://cybercrime-tracker.net/ccpm.php",
          "malware.hash.md5": "29affc7996f4a736956a0d890684cde7",
          "source.fqdn": "asigurari-daune-despagubiri.ro",
          "source.url": "http://asigurari-daune-despagubiri.ro/wp-database/stainman/gate.php"}


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
