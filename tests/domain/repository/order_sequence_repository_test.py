from application.domain.repository.order_sequence_repository import OrderSequenceRepository
from tests import BaseTestCase


class OrderSequenceTests(BaseTestCase):

    def setUp(self):
        super(OrderSequenceTests, self).setUp()
        self.order_sequence_repository = OrderSequenceRepository()

    def tearDown(self):
        super(OrderSequenceTests, self).tearDown()

    def test_find_by_fiscal_year(self):
        before = len(self.order_sequence_repository.find_all())
        order_sequence = self.order_sequence_repository.find_by_fiscal_year(99)
        self.assertEqual(order_sequence.fiscal_year, 99)

        # 件数が増えていることを確認
        after = len(self.order_sequence_repository.find_all())
        self.assertEqual(before, after)

    def test_create(self):
        order_sequence = self.order_sequence_repository.create()
        self.assertIsNone(order_sequence.id)
