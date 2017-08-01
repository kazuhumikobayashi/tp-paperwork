from datetime import datetime

from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.immutables.tax import Tax
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
            billing_input_flag=0,
            deposit_input_flag=0,
            deposit_date='2017/1/1',
            billing_estimated_money=10000,
            billing_confirmation_money=10000,
            billing_tax=Tax.eight,
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
                   "', billing_input_flag='{}".format(project_month.billing_input_flag) + \
                   "', deposit_input_flag='{}".format(project_month.deposit_input_flag) + \
                   "', deposit_date='{}".format(project_month.deposit_date) + \
                   "', billing_estimated_money='{}".format(project_month.billing_estimated_money) + \
                   "', billing_confirmation_money='{}".format(project_month.billing_confirmation_money) + \
                   "', billing_tax='{}".format(project_month.billing_tax) + \
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
        project_month = ProjectMonth(
            project_id=1,
            project_month='2017/1/1',
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

        # 消費税率が0のとき、消費税は0円となる。
        expected = 0
        project_month.billing_tax = Tax.zero
        actual = project_month.tax_of_billing_confirmation_money()
        self.assertEqual(expected, actual)

        # billing_confirmation_moneyが1000000なので、消費税率が8%のときは消費税が80000円となる。
        expected = 80000
        project_month.billing_tax = Tax.eight
        actual = project_month.tax_of_billing_confirmation_money()
        self.assertEqual(expected, actual)

        # billing_confirmation_moneyが1000000なので、消費税率が10%のときは消費税が100000円となる。
        expected = 100000
        project_month.billing_tax = Tax.ten
        actual = project_month.tax_of_billing_confirmation_money()
        self.assertEqual(expected, actual)
