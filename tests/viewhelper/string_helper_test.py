import unittest

from markupsafe import Markup

from application.viewhelper import filter_suppress_none, with_yen
from application.viewhelper import number_with_commas


class StringHelperTests(unittest.TestCase):

    def test_filter_suppress_none(self):
        expected = ''
        actual = filter_suppress_none(None)
        self.assertEqual(actual, expected)

    def test_filter_suppress_not_none(self):
        expected = 'test'
        actual = filter_suppress_none('test')
        self.assertEqual(actual, expected)

    def test_number_with_commas(self):
        expected = '3,000'
        actual = number_with_commas(3000)
        self.assertEqual(actual, expected)

    def test_number_with_commas_none(self):
        expected = ''
        actual = number_with_commas(None)
        self.assertEqual(actual, expected)

    def test_with_yen(self):
        expected = Markup('&yen1000')
        actual = with_yen('1000')
        self.assertEqual(actual, expected)

    def test_with_yen_none(self):
        expected = ''
        actual = with_yen(None)
        self.assertEqual(actual, expected)
