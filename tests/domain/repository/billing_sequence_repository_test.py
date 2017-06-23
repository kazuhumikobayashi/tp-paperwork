from application.domain.repository.billing_sequence_repository import BillingSequenceRepository
from tests import BaseTestCase


class BillingSequenceTests(BaseTestCase):

    def setUp(self):
        super(BillingSequenceTests, self).setUp()
        self.billing_sequence_repository = BillingSequenceRepository()

    def tearDown(self):
        super(BillingSequenceTests, self).tearDown()

    def test_find_by_fiscal_year(self):
        before = len(self.billing_sequence_repository.find_all())
        billing_sequence = self.billing_sequence_repository.find_by_fiscal_year(99)
        self.assertEqual(billing_sequence.fiscal_year, 99)

        # 件数が増えていることを確認
        after = len(self.billing_sequence_repository.find_all())
        self.assertEqual(before, after)

    def test_create(self):
        billing_sequence = self.billing_sequence_repository.create()
        self.assertIsNone(billing_sequence.id)
