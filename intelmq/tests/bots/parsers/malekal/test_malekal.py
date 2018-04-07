# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.malekal.parser import MalekalParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'test_malekal.data'), 'rb') as handle:
    REPORT_DATA = handle.read()


REPORT = {"__type": "Report",
          "feed.name": "malekal malwaredb feed",
          "feed.url": "http://malwaredb.malekal.com/index.php?page=31",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-04-07T07:36:53+00:00"
          }
EVENT1 = {"time.observation": "2018-04-07T07:36:53+00:00",
          "feed.url": "http://malwaredb.malekal.com/index.php?page=31",
          "feed.name": "malekal malwaredb feed",
          "extra.rate": "7/56 ",
          "extra.size": "197887",
          "malware.hash.md5": "df0198d5368df1cd600292fcc77cd45e",
          "malware.hash.sha1": "544478b0a0966634958c72f6ad5292626a95d8bd",
          "malware.hash.sha256": "8c306d794e0eb33e24e252f51aa19964c0f5a04cac742396f4b570a2c7b48ca9",
          "malware.name": "kaspersky: uds:dangerousobject.multi.generic",
          "raw": "PHRkIGFsaWduPSJjZW50ZXIiIG5vd3JhcD0iIj5XZWQsIDMwIE1hciAyMDE2IDEwOjI1OjE3ICswMjAwPC90Z"
                 "D48dGQgbm93cmFwPSIiPjxiPk1ENTo8L2I+IDxhIGhyZWY9Imh0dHA6Ly9tYWx3YXJlZGIubWFsZWthbC5jb20"
                 "vaW5kZXgucGhwP2hhc2g9ZGYwMTk4ZDUzNjhkZjFjZDYwMDI5MmZjYzc3Y2Q0NWUiPmRmMDE5OGQ1MzY4ZGYxY2Q"
                 "2MDAyOTJmY2M3N2NkNDVlPC9hPjxici8+CgkJPGI+U0hBMTo8L2I+IDxhIGhyZWY9Imh0dHA6Ly9zZWN1Ym94bGF"
                 "icy5mci9rb2xhYi9hcGk/aGFzaD01NDQ0NzhiMGEwOTY2NjM0OTU4YzcyZjZhZDUyOTI2MjZhOTVkOGJkIj41NDQ"
                 "0NzhiMGEwOTY2NjM0OTU4YzcyZjZhZDUyOTI2MjZhOTVkOGJkPC9hPjxici8+CgkJPGI+U0hBMjU2OjwvYj4gPGE"
                 "gaHJlZj0iaHR0cDovL21hbHdhcmVkYi5tYWxla2FsLmNvbS9pbmRleC5waHA/aGFzaD04YzMwNmQ3OTRlMGViMzNl"
                 "MjRlMjUyZjUxYWExOTk2NGMwZjVhMDRjYWM3NDIzOTZmNGI1NzBhMmM3YjQ4Y2E5Ij44YzMwNmQ3OTRlMGViMzNlMjRlMjUyZj"
                 "UxYWExOTk2NGMwZjVhMDRjYWM3NDIzOTZmNGI1NzBhMmM3YjQ4Y2E5PC9hPgoJICAgICAgPC90ZD48dGQgYWxpZ249ImNlbnRl"
                 "ciI+MTk3ODg3PC90ZD48dGQgYWxpZ249ImxlZnQiPmthc3BlcnNreTogVURTOkRhbmdlcm91c09iamVjdC5NdWx0aS5HZW5lcm"
                 "ljPGJyLz48L3RkPjx0ZCBhbGlnbj0iY2VudGVyIiBub3dyYXA9IiI+PGI+RmlsZSBkZXRlY3Rpb24gOjwvYj4gPGEgaHJlZj0i"
                 "aHR0cDovL3d3dy52aXJ1c3RvdGFsLmNvbS9sYXRlc3QtcmVwb3J0Lmh0bWw/cmVzb3VyY2U9NTQ0NDc4YjBhMDk2NjYzNDk1OG"
                 "M3MmY2YWQ1MjkyNjI2YTk1ZDhiZCI+PGZvbnQgY29sb3I9InJlZCI+Ny81NiAoMTMlKSAyMDE2LTAzLTMwIDA4OjQyOjI1PC9m"
                 "b250PjwvYT48YnIvPjxici8+U2FuZGJveCA6IDxhIGhyZWY9Imh0dHA6Ly9jYW1hcy5jb21vZG8uY29tL2NnaS1iaW4vc3VibWl"
                 "0P2ZpbGU9OGMzMDZkNzk0ZTBlYjMzZTI0ZTI1MmY1MWFhMTk5NjRjMGY1YTA0Y2FjNzQyMzk2ZjRiNTcwYTJjN2I0OGNhOSI+Q0F"
                 "NQVM8L2E+PC90ZD48dGQgYWxpZ249ImNlbnRlciI+Ti9BPGJyLz48L3RkPg==",
          "time.source": "2016-03-30T08:25:17+00:00",
          "classification.type": "malware",
          "__type": "Event"}


class TestMalekalParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MalekalParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)


if __name__ == '__main__':
    unittest.main()
