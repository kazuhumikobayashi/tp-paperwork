from application.domain.model.project_result import ProjectResult
from tests import BaseTestCase


class ProjectResultTests(BaseTestCase):

    def setUp(self):
        super(ProjectResultTests, self).setUp()

    def tearDown(self):
        super(ProjectResultTests, self).tearDown()

    def test___repr__(self):
        project_result = ProjectResult(
                 project_detail_id=1,
                 result_month='2017/1/1',
                 work_time=1,
                 billing_transportation=2,
                 billing_adjustments=3,
                 billing_confirmation_number=4,
                 billing_confirmation_money=5,
                 payment_transportation=6,
                 payment_adjustments=7,
                 payment_confirmation_money=8,
                 remarks='test',
                 billing_receipted_date=None,
                 payment_expected_date=None,
                 payment_flag=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None)
        
        expected = "<ProjectResult:" + \
                   "'id='{}".format(project_result.id) + \
                   "', project_detail_id='{}".format(project_result.project_detail_id) + \
                   "', result_month='{}".format(project_result.result_month) + \
                   "', work_time='{}".format(project_result.work_time) + \
                   "', billing_transportation='{}".format(project_result.billing_transportation) + \
                   "', billing_adjustments='{}".format(project_result.billing_adjustments) + \
                   "', billing_confirmation_number='{}".format(project_result.billing_confirmation_number) + \
                   "', billing_confirmation_money='{}".format(project_result.billing_confirmation_money) + \
                   "', payment_transportation='{}".format(project_result.payment_transportation) + \
                   "', payment_adjustments='{}".format(project_result.payment_adjustments) + \
                   "', payment_confirmation_money='{}".format(project_result.payment_confirmation_money) + \
                   "', remarks='{}".format(project_result.remarks) + \
                   "', billing_receipted_date='{}".format(project_result.billing_receipted_date) + \
                   "', payment_expected_date='{}".format(project_result.payment_expected_date) + \
                   "', payment_flag='{}".format(project_result.payment_flag) + \
                   "', created_at='{}".format(project_result.created_at) + \
                   "', created_user='{}".format(project_result.created_user) + \
                   "', updated_at='{}".format(project_result.updated_at) + \
                   "', updated_user='{}".format(project_result.updated_user) + \
                   "'>"
        actual = str(project_result)
        self.assertEqual(actual, expected)
