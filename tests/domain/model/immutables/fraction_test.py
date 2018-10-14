import unittest

from application.domain.model.immutables.fraction import Fraction


class FractionTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Fraction.one.name, '1の位')
        self.assertEqual(Fraction.ten.name, '10の位')
        self.assertEqual(Fraction.hundred.name, '100の位')
        self.assertEqual(Fraction.thousand.name, '1000の位')

    def test_parse(self):
        one = -1
        ten = -2
        hundred = -3
        thousand = -4

        self.assertEqual(Fraction.parse(one), Fraction.one)
        self.assertEqual(Fraction.parse(ten), Fraction.ten)
        self.assertEqual(Fraction.parse(hundred), Fraction.hundred)
        self.assertEqual(Fraction.parse(thousand), Fraction.thousand)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Fraction.parse(0))
        self.assertIsNone(Fraction.parse('a'))

    def test_str(self):
        one = '-1'
        ten = '-2'
        hundred = '-3'
        thousand = '-4'

        self.assertEqual(str(Fraction.one), one)
        self.assertEqual(str(Fraction.ten), ten)
        self.assertEqual(str(Fraction.hundred), hundred)
        self.assertEqual(str(Fraction.thousand), thousand)
