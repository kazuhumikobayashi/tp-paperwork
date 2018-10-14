import unittest

from application.domain.model.immutables.gender import Gender


class GenderTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Gender.male.name, '男性')
        self.assertEqual(Gender.female.name, '女性')

    def test_parse(self):
        male = 1
        female = 2

        self.assertEqual(Gender.parse(male), Gender.male)
        self.assertEqual(Gender.parse(female), Gender.female)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Gender.parse(0))
        self.assertIsNone(Gender.parse('a'))
