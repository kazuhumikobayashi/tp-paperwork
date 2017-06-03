from application.domain.model.immutables.expression import Expression
from tests import BaseTestCase


class ExpressionTests(BaseTestCase):

    def setUp(self):
        super(ExpressionTests, self).setUp()

    def tearDown(self):
        super(ExpressionTests, self).tearDown()

    def test_name(self):
        self.assertEqual(Expression.more.name, '以上')
        self.assertEqual(Expression.more_than.name, 'より大きい')
        self.assertEqual(Expression.less.name, '以下')
        self.assertEqual(Expression.less_than.name, '未満')

    def test_parse(self):
        more = 1
        more_than = 2
        less = 3
        less_than = 4

        self.assertEquals(Expression.parse(more), Expression.more)
        self.assertEquals(Expression.parse(more_than), Expression.more_than)
        self.assertEquals(Expression.parse(less), Expression.less)
        self.assertEquals(Expression.parse(less_than), Expression.less_than)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Expression.parse(0))
        self.assertIsNone(Expression.parse('a'))

    def test_str(self):
        more = '1'
        more_than = '2'
        less = '3'
        less_than = '4'

        self.assertEquals(str(Expression.more), more)
        self.assertEquals(str(Expression.more_than), more_than)
        self.assertEquals(str(Expression.less), less)
        self.assertEquals(str(Expression.less_than), less_than)
