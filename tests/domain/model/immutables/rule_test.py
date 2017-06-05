from application.domain.model.immutables.rule import Rule
from tests import BaseTestCase


class RuleTests(BaseTestCase):

    def setUp(self):
        super(RuleTests, self).setUp()

    def tearDown(self):
        super(RuleTests, self).tearDown()

    def test_name(self):
        self.assertEqual(Rule.fixed.name, '固定')
        self.assertEqual(Rule.variable.name, '変動')

    def test_parse(self):
        fixed = 1
        variable = 2

        self.assertEquals(Rule.parse(fixed), Rule.fixed)
        self.assertEquals(Rule.parse(variable), Rule.variable)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Rule.parse(0))
        self.assertIsNone(Rule.parse('a'))

    def test_str(self):
        fixed = '1'
        variable = '2'

        self.assertEqual(str(Rule.fixed), fixed)
        self.assertEqual(str(Rule.variable), variable)