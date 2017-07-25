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
            project = self.project_month_repository.find_by_id(1)
            user = self.user_repository.find_by_id(1)
            session['user'] = user.serialize()
            billing_base_report = BillingBaseReport(project)
        self.billing_base_report = billing_base_report

    def tearDown(self):
        super(BillingBaseReportTests, self).tearDown()

    def test_write_estimated_content_rows_if_blanket(self):

        # テスト対象のメソッドを実行
        self.billing_base_report.create_billing_details()
