import datetime

from application.viewhelper import datetime_format
from tests import BaseTestCase


class DateHelperTests(BaseTestCase):

    def setUp(self):
        super(DateHelperTests, self).setUp()

    def tearDown(self):
        super(DateHelperTests, self).tearDown()

    def test_datetime_format(self):
        expected = datetime.datetime.now().strftime('%Y/%m/%d')
        actual = datetime_format(datetime.datetime.now(), '%Y/%m/%d')
        self.assertEqual(actual, expected)

    def test_datetime_format_none(self):
        expected = ''
        actual = datetime_format(None, '%Y/%m/%d')
        self.assertEqual(actual, expected)
