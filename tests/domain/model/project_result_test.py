from application.domain.model.project_result import ProjectResult
from application.domain.repository.project_result_repository import ProjectResultRepository
from tests import BaseTestCase


class ProjectResultTests(BaseTestCase):

    def setUp(self):
        super(ProjectResultTests, self).setUp()
        self.project_result_repository = ProjectResultRepository()

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

    # 技術者履歴がない場合、taxの値は0になる
    def test_tax_of_payment_confirmation_money_if_no_history(self):
        project_result = self.project_result_repository.find_all()[0]
        expected = 0

        actual = project_result.tax_of_payment_confirmation_money(engineer_history=None)

        self.assertEqual(expected, actual)
