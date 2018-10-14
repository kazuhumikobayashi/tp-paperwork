import unittest

from application.domain.model.immutables.week import Week


class WeekTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Week.monday.name, '月曜日')
        self.assertEqual(Week.tuesday.name, '火曜日')
        self.assertEqual(Week.wednesday.name, '水曜日')
        self.assertEqual(Week.thursday.name, '木曜日')
        self.assertEqual(Week.friday.name, '金曜日')
        self.assertEqual(Week.saturday.name, '土曜日')
        self.assertEqual(Week.sunday.name, '日曜日')

    def test_short_name(self):
        self.assertEqual(Week.monday.short_name, '月')
        self.assertEqual(Week.tuesday.short_name, '火')
        self.assertEqual(Week.wednesday.short_name, '水')
        self.assertEqual(Week.thursday.short_name, '木')
        self.assertEqual(Week.friday.short_name, '金')
        self.assertEqual(Week.saturday.short_name, '土')
        self.assertEqual(Week.sunday.short_name, '日')

    def test_parse(self):
        monday = 0
        tuesday = 1
        wednesday = 2
        thursday = 3
        friday = 4
        saturday = 5
        sunday = 6

        self.assertEqual(Week.parse(monday), Week.monday)
        self.assertEqual(Week.parse(tuesday), Week.tuesday)
        self.assertEqual(Week.parse(wednesday), Week.wednesday)
        self.assertEqual(Week.parse(thursday), Week.thursday)
        self.assertEqual(Week.parse(friday), Week.friday)
        self.assertEqual(Week.parse(saturday), Week.saturday)
        self.assertEqual(Week.parse(sunday), Week.sunday)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Week.parse(10))
        self.assertIsNone(Week.parse('a'))

    def test_str(self):
        monday = '0'
        tuesday = '1'
        wednesday = '2'
        thursday = '3'
        friday = '4'
        saturday = '5'
        sunday = '6'

        self.assertEqual(str(Week.monday), monday)
        self.assertEqual(str(Week.tuesday), tuesday)
        self.assertEqual(str(Week.wednesday), wednesday)
        self.assertEqual(str(Week.thursday), thursday)
        self.assertEqual(str(Week.friday), friday)
        self.assertEqual(str(Week.saturday), saturday)
        self.assertEqual(str(Week.sunday), sunday)
