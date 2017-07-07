from application.domain.repository.estimation_sequence_repository import EstimationSequenceRepository
from tests import BaseTestCase


class EstimationSequenceTests(BaseTestCase):

    def setUp(self):
        super(EstimationSequenceTests, self).setUp()
        self.estimation_sequence_repository = EstimationSequenceRepository()

    def tearDown(self):
        super(EstimationSequenceTests, self).tearDown()

    def test_find_by_fiscal_year(self):
        before = len(self.estimation_sequence_repository.find_all())
        estimation_sequence = self.estimation_sequence_repository.find_by_fiscal_year(99)
        self.assertEqual(estimation_sequence.fiscal_year, 99)

        # 件数が増えていることを確認
        after = len(self.estimation_sequence_repository.find_all())
        self.assertEqual(before, after)

    def test_create(self):
        estimation_sequence = self.estimation_sequence_repository.create()
        self.assertIsNone(estimation_sequence.id)
