import unittest

from application.domain.model.immutables.site import Site


class SiteTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Site.zero.name, '0')
        self.assertEqual(Site.ten.name, '10')
        self.assertEqual(Site.twenty_five.name, '25')
        self.assertEqual(Site.thirty.name, '30')
        self.assertEqual(Site.thirty_five.name, '35')
        self.assertEqual(Site.forty.name, '40')
        self.assertEqual(Site.forty_five.name, '45')
        self.assertEqual(Site.fifty.name, '50')
        self.assertEqual(Site.fifty_one.name, '51')
        self.assertEqual(Site.fifty_five.name, '55')
        self.assertEqual(Site.sixty.name, '60')

    def test_parse(self):
        zero = 0
        ten = 10
        twenty_five = 25
        thirty = 30
        thirty_five = 35
        forty = 40
        forty_five = 45
        fifty = 50
        fifty_one = 51
        fifty_five = 55
        sixty = 60

        self.assertEqual(Site.parse(zero), Site.zero)
        self.assertEqual(Site.parse(ten), Site.ten)
        self.assertEqual(Site.parse(twenty_five), Site.twenty_five)
        self.assertEqual(Site.parse(thirty), Site.thirty)
        self.assertEqual(Site.parse(thirty_five), Site.thirty_five)
        self.assertEqual(Site.parse(forty), Site.forty)
        self.assertEqual(Site.parse(forty_five), Site.forty_five)
        self.assertEqual(Site.parse(fifty), Site.fifty)
        self.assertEqual(Site.parse(fifty_one), Site.fifty_one)
        self.assertEqual(Site.parse(fifty_five), Site.fifty_five)
        self.assertEqual(Site.parse(sixty), Site.sixty)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Site.parse(-1))
        self.assertIsNone(Site.parse('a'))

    def test_str(self):
        zero = '0'
        ten = '10'
        twenty_five = '25'
        thirty = '30'
        thirty_five = '35'
        forty = '40'
        forty_five = '45'
        fifty = '50'
        fifty_one = '51'
        fifty_five = '55'
        sixty = '60'

        self.assertEqual(str(Site.zero), zero)
        self.assertEqual(str(Site.ten), ten)
        self.assertEqual(str(Site.twenty_five), twenty_five)
        self.assertEqual(str(Site.thirty), thirty)
        self.assertEqual(str(Site.thirty_five), thirty_five)
        self.assertEqual(str(Site.forty), forty)
        self.assertEqual(str(Site.forty_five), forty_five)
        self.assertEqual(str(Site.fifty), fifty)
        self.assertEqual(str(Site.fifty_one), fifty_one)
        self.assertEqual(str(Site.fifty_five), fifty_five)
        self.assertEqual(str(Site.sixty), sixty)
