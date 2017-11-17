from datetime import datetime, date

from application import db
from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.engineer import Engineer
from application.domain.model.engineer_history import EngineerHistory
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.tax import Tax
from application.domain.repository.engineer_repository import EngineerRepository
from tests import BaseTestCase


class EngineerTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(EngineerTests, cls).setUpClass()

    def setUp(self):
        super(EngineerTests, self).setUp()
        self.engineer_repository = EngineerRepository()

    def tearDown(self):
        super(EngineerTests, self).tearDown()

    def test_get_histories_by_date_is_none(self):
        # set_up
        company = Company(
            company_name='会社',
            contract_date=datetime.today().strftime('%Y/%m/%d'),
            payment_site=Site.fifty,
            payment_tax=Tax.eight,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='エンジニア',
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        history = EngineerHistory(
            engineer_id=engineer.id,
            payment_start_day=date(2016, 1, 1),
            payment_end_day=date(2016, 12, 31),
            payment_per_month=600000,
            payment_rule=Rule.fixed,
            payment_site=engineer.company.payment_site,
            payment_tax=engineer.company.payment_tax,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(history)
        db.session.commit()

        self.assertIsNone(engineer.get_payment_site_by_date(date(2017, 1, 1)))
