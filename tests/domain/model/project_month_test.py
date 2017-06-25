from datetime import datetime, date

from application import db
from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.immutables.status import Status
from application.domain.model.immutables.tax import Tax
from application.domain.model.project import Project
from application.domain.model.project_month import ProjectMonth
from tests import BaseTestCase


class ProjectMonthTests(BaseTestCase):

    def setUp(self):
        super(ProjectMonthTests, self).setUp()

    def tearDown(self):
        super(ProjectMonthTests, self).tearDown()

    def test___repr__(self):
        project_month = ProjectMonth(
            project_id=1,
            project_month='2017/1/1',
            result_input_flag=0,
            billing_input_flag=0,
            deposit_input_flag=0,
            deposit_date='2017/1/1',
            billing_estimated_money=10000,
            billing_confirmation_money=10000,
            billing_transportation=100,
            remarks='remarks',
            client_billing_no=None,
            created_at=None,
            created_user=None,
            updated_at=None,
            updated_user=None)

        expected = "<ProjectMonth:" + \
                   "'id='{}".format(project_month.id) + \
                   "', project_id='{}".format(project_month.project_id) + \
                   "', project_month='{}".format(project_month.project_month) + \
                   "', result_input_flag='{}".format(project_month.result_input_flag) + \
                   "', billing_input_flag='{}".format(project_month.billing_input_flag) + \
                   "', deposit_input_flag='{}".format(project_month.deposit_input_flag) + \
                   "', deposit_date='{}".format(project_month.deposit_date) + \
                   "', billing_estimated_money='{}".format(project_month.billing_estimated_money) + \
                   "', billing_confirmation_money='{}".format(project_month.billing_confirmation_money) + \
                   "', billing_transportation='{}".format(project_month.billing_transportation) + \
                   "', remarks='{}".format(project_month.remarks) + \
                   "', client_billing_no='{}".format(project_month.client_billing_no) + \
                   "', created_at='{}".format(project_month.created_at) + \
                   "', created_user='{}".format(project_month.created_user) + \
                   "', updated_at='{}".format(project_month.updated_at) + \
                   "', updated_user='{}".format(project_month.updated_user) + \
                   "'>"

        actual = str(project_month)
        self.assertEqual(actual, expected)

    def test_tax_of_billing_confirmation_money(self):
        # set_up
        company = Company(
            company_name='顧客会社',
            contract_date=datetime.today().strftime('%Y/%m/%d'),
            billing_tax=Tax.zero,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.client,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        project = Project(
                    project_name='test_project',
                    project_name_for_bp='project',
                    status=Status.start,
                    recorded_department_id=1,
                    sales_person='営業担当',
                    estimation_no='M2000',
                    end_user_company_id=1,
                    client_company_id=company.id,
                    start_date=date.today(),
                    end_date='2099/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    estimated_total_amount=1000000,
                    scope='test',
                    contents=None,
                    working_place=None,
                    delivery_place=None, deliverables=None,
                    inspection_date=None,
                    responsible_person=None,
                    quality_control=None, subcontractor=None,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_month = ProjectMonth(
            project_id=project.id,
            project_month='2017/1/1',
            result_input_flag=InputFlag.yet,
            billing_input_flag=InputFlag.yet,
            deposit_input_flag=InputFlag.yet,
            deposit_date='2017/1/1',
            billing_estimated_money=None,
            billing_confirmation_money=1000000,
            billing_transportation=None,
            remarks='remarks',
            client_billing_no=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project_month)
        db.session.commit()

        # 消費税率が0のとき、消費税は0円となる。
        expected = 0
        project_month.project.client_company.billing_tax = Tax.zero
        actual = project_month.tax_of_billing_confirmation_money()
        self.assertEqual(expected, actual)

        # billing_confirmation_moneyが1000000なので、消費税率が8%のときは消費税が80000円となる。
        expected = 80000
        project_month.project.client_company.billing_tax = Tax.eight
        actual = project_month.tax_of_billing_confirmation_money()
        self.assertEqual(expected, actual)

        # billing_confirmation_moneyが1000000なので、消費税率が10%のときは消費税が100000円となる。
        expected = 100000
        project_month.project.client_company.billing_tax = Tax.ten
        actual = project_month.tax_of_billing_confirmation_money()
        self.assertEqual(expected, actual)

        db.session.delete(project_month)
        db.session.delete(project)
        db.session.delete(company_client_flag)
        db.session.delete(company)
        db.session.commit()
