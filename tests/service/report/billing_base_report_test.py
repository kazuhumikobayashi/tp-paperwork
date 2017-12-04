import locale

from flask import session

from application import app
from application.domain.repository.project_month_repository import ProjectMonthRepository
from application.domain.repository.user_repository import UserRepository
from application.service.report.billing_base_report import BillingBaseReport
from tests import BaseTestCase


class BillingBaseReportTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(BillingBaseReportTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BillingBaseReportTests, cls).tearDownClass()

    def setUp(self):
        super(BillingBaseReportTests, self).setUp()
        self.project_month_repository = ProjectMonthRepository()
        self.user_repository = UserRepository()
        with app.test_request_context():
            project_month = self.project_month_repository.find_by_id(1)
            project_month.remarks = 'test'
            user = self.user_repository.find_by_id(1)
            session['user'] = user.serialize()
            billing_base_report = BillingBaseReport(project_month)
        self.billing_base_report = billing_base_report

    def tearDown(self):
        super(BillingBaseReportTests, self).tearDown()

    def test_write_estimated_content_rows_if_blanket(self):
        # テスト対象のメソッドを実行
        self.billing_base_report.create_billing_details()

    def test_remark(self):
        locale.setlocale(locale.LC_ALL, '')
        deposit_date = self.billing_base_report.project_month.deposit_date.strftime('%Y年%m月%d日')

        expected = "お支払いは下記口座に{}までにお支払い願います。\n\n".format(deposit_date)
        if self.billing_base_report.project_month.remarks:
            expected += self.billing_base_report.project_month.remarks + '\n'
        if self.billing_base_report.project_month.project.client_order_no:
            expected += "※作業内容及び納品物等の詳細はご注文書（No.{}）の通り"\
                 .format(self.billing_base_report.project_month.project.client_order_no)

        # テスト対象のメソッドを実行
        actual = self.billing_base_report.remark()
        self.assertEqual(expected, actual)
