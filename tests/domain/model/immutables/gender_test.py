from application.domain.model.immutables.gender import Gender
from tests import BaseTestCase


class GenderTests(BaseTestCase):

    def setUp(self):
        super(GenderTests, self).setUp()

    def tearDown(self):
        super(GenderTests, self).tearDown()

    def test_name(self):
        self.assertEqual(Gender.male.name, '男性')
        self.assertEqual(Gender.female.name, '女性')

    def test_parse(self):
        male = 1
        female = 2

        self.assertEquals(Gender.parse(male), Gender.male)
        self.assertEquals(Gender.parse(female), Gender.female)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Gender.parse(0))
        self.assertIsNone(Gender.parse('a'))
