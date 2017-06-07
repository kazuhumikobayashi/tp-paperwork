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
            payment_input_flag=0,
            payment_date='2017/1/1',
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
                   "', payment_input_flag='{}".format(project_month.payment_input_flag) + \
                   "', payment_date='{}".format(project_month.payment_date) + \
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
