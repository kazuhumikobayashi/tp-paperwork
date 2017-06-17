import datetime
import unittest

from application.viewhelper import datetime_format


class DateHelperTests(unittest.TestCase):

    def test_datetime_format(self):
        expected = datetime.datetime.now().strftime('%Y/%m/%d')
        actual = datetime_format(datetime.datetime.now(), '%Y/%m/%d')
        self.assertEqual(actual, expected)

    def test_datetime_format_none(self):
        expected = ''
        actual = datetime_format(None, '%Y/%m/%d')
        self.assertEqual(actual, expected)
