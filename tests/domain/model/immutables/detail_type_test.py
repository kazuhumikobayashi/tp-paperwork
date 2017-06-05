from application.domain.model.immutables.detail_type import DetailType
from tests import BaseTestCase


class DetailTypeTests(BaseTestCase):

    def setUp(self):
        super(DetailTypeTests, self).setUp()

    def tearDown(self):
        super(DetailTypeTests, self).tearDown()

    def test_name(self):
        self.assertEqual(DetailType.engineer.name, '技術者')
        self.assertEqual(DetailType.work.name, '作業')

    def test_parse(self):
        engineer = 1
        work = 2

        self.assertEquals(DetailType.parse(engineer), DetailType.engineer)
        self.assertEquals(DetailType.parse(work), DetailType.work)

    def test_parse_fail_is_none(self):
        self.assertIsNone(DetailType.parse(0))
        self.assertIsNone(DetailType.parse('a'))

    def test_str(self):
        engineer = '1'
        work = '2'

        self.assertEqual(str(DetailType.engineer), engineer)
        self.assertEqual(str(DetailType.work), work)
