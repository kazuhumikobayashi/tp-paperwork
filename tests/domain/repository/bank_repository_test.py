from application.domain.repository.bank_repository import BankRepository
from tests import BaseTestCase


class BankRepositoryTests(BaseTestCase):

    def setUp(self):
        super(BankRepositoryTests, self).setUp()
        self.bank_repository = BankRepository()

    def tearDown(self):
        super(BankRepositoryTests, self).tearDown()

    def test_create(self):
        bank = self.bank_repository.create()
        self.assertIsNone(bank.id)
