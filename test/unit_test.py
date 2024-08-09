import unittest
from spack_commands import time_format


class TimeFormatTest(unittest.TestCase):
    def test_example(self):
        self.assertEqual(time_format(0.123), "0.12s")
        self.assertEqual(time_format(123.456), "2m 3.46s")
        self.assertEqual(time_format(123456.789), "34h 17m 36.79s")
