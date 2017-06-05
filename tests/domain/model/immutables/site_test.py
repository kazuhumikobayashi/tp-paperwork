from application.domain.model.immutables.site import Site
from tests import BaseTestCase


class SiteTests(BaseTestCase):

    def setUp(self):
        super(SiteTests, self).setUp()

    def tearDown(self):
        super(SiteTests, self).tearDown()

    def test_name(self):
        self.assertEqual(Site.twenty_five.name, '25')
        self.assertEqual(Site.thirty.name, '30')
        self.assertEqual(Site.forty.name, '40')
        self.assertEqual(Site.fifty.name, '50')
        self.assertEqual(Site.fifty_one.name, '51')
        self.assertEqual(Site.fifty_five.name, '55')
        self.assertEqual(Site.sixty.name, '60')

    def test_parse(self):
        twenty_five = 25
        thirty = 30
        forty = 40
        fifty = 50
        fifty_one = 51
        fifty_five = 55
        sixty = 60

        self.assertEquals(Site.parse(twenty_five), Site.twenty_five)
        self.assertEquals(Site.parse(thirty), Site.thirty)
        self.assertEquals(Site.parse(forty), Site.forty)
        self.assertEquals(Site.parse(fifty), Site.fifty)
        self.assertEquals(Site.parse(fifty_one), Site.fifty_one)
        self.assertEquals(Site.parse(fifty_five), Site.fifty_five)
        self.assertEquals(Site.parse(sixty), Site.sixty)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Site.parse(0))
        self.assertIsNone(Site.parse('a'))

    def test_str(self):
        twenty_five = '25'
        thirty = '30'
        forty = '40'
        fifty = '50'
        fifty_one = '51'
        fifty_five = '55'
        sixty = '60'

        self.assertEquals(str(Site.twenty_five), twenty_five)
        self.assertEquals(str(Site.thirty), thirty)
        self.assertEquals(str(Site.forty), forty)
        self.assertEquals(str(Site.fifty), fifty)
        self.assertEquals(str(Site.fifty_one), fifty_one)
        self.assertEquals(str(Site.fifty_five), fifty_five)
        self.assertEquals(str(Site.sixty), sixty)