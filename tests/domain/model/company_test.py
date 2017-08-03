from datetime import datetime

from application.domain.model.company import Company
from application.domain.repository.company_repository import CompanyRepository
from tests import BaseTestCase


class CompanyTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(CompanyTests, cls).setUpClass()

    def setUp(self):
        super(CompanyTests, self).setUp()
        self.company_repository = CompanyRepository()

    def tearDown(self):
        super(CompanyTests, self).tearDown()

    def test_has_relationship(self):
        company = self.company_repository.find_by_id(1)

        self.assertTrue(company.has_relationship())

    def test_has_no_relationship(self):
        company = Company(
            company_name='テスト会社',
            contract_date=datetime.today().strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test'
        )

        self.assertFalse(company.has_relationship())
