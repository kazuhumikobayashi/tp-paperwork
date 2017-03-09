from application.domain.repository.contract_form_repository import ContractFormRepository
from tests import BaseTestCase


class ContractFormRepositoryTests(BaseTestCase):

    def setUp(self):
        super(ContractFormRepositoryTests, self).setUp()
        self.contract_form_repository = ContractFormRepository()

    def tearDown(self):
        super(ContractFormRepositoryTests, self).tearDown()

    def test_find_by_name(self):
        expected = '一括'
        contract_form = self.contract_form_repository.find_by_name(expected)
        actual = contract_form.contract_form_name
        self.assertEqual(actual, expected)

    def test_create(self):
        contract_form = self.contract_form_repository.create()
        self.assertIsNone(contract_form.id)
