from application.domain.model.immutables.holiday_flag import HolidayFlag
from tests import BaseTestCase


class HolidayFlagTests(BaseTestCase):

    def setUp(self):
        super(HolidayFlagTests, self).setUp()

    def tearDown(self):
        super(HolidayFlagTests, self).tearDown()

    def test_name(self):
        self.assertEqual(HolidayFlag.before.name, '前倒し')
        self.assertEqual(HolidayFlag.after.name, '後ろ倒し')

    def test_parse(self):
        before = -1
        after = 1

        self.assertEquals(HolidayFlag.parse(before), HolidayFlag.before)
        self.assertEquals(HolidayFlag.parse(after), HolidayFlag.after)

    def test_parse_fail_is_none(self):
        self.assertIsNone(HolidayFlag.parse(0))
        self.assertIsNone(HolidayFlag.parse('a'))

    def test_str(self):
        before = '-1'
        after = '1'

        self.assertEqual(str(HolidayFlag.before), before)
        self.assertEqual(str(HolidayFlag.after), after)
