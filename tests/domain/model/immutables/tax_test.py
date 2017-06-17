import unittest

from application.domain.model.immutables.tax import Tax


class TaxTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Tax.zero.name, 'なし')
        self.assertEqual(Tax.eight.name, '8％')
        self.assertEqual(Tax.ten.name, '10％')

    def test_parse(self):
        zero = 0
        eight = 8
        ten = 10

        self.assertEquals(Tax.parse(zero), Tax.zero)
        self.assertEquals(Tax.parse(eight), Tax.eight)
        self.assertEquals(Tax.parse(ten), Tax.ten)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Tax.parse(3))
        self.assertIsNone(Tax.parse('a'))
