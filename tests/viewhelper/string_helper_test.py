from application.viewhelper import filter_suppress_none
from application.viewhelper import number_with_commas
from tests import BaseTestCase


class StringHelperTests(BaseTestCase):

    def setUp(self):
        super(StringHelperTests, self).setUp()

    def tearDown(self):
        super(StringHelperTests, self).tearDown()

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
