from datetime import datetime, date

from flask import session

from application import app, db
from application.domain.model.engineer_history import EngineerHistory
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.tax import Tax
from application.domain.repository.engineer_repository import EngineerRepository
from application.domain.repository.project_detail_repository import ProjectDetailRepository
from application.domain.repository.project_repository import ProjectRepository
from application.domain.repository.user_repository import UserRepository
from application.service.report.bp_order_report import BpOrderReport
from tests import BaseTestCase


class BpOrderReportTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(BpOrderReportTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BpOrderReportTests, cls).tearDownClass()

    def setUp(self):
        super(BpOrderReportTests, self).setUp()
        self.project_repository = ProjectRepository()
        self.user_repository = UserRepository()
        self.project_detail_repository = ProjectDetailRepository()
        self.engineer_repository = EngineerRepository()
        with app.test_request_context():
            project_detail = self.project_detail_repository.find_by_id(1)
            user = self.user_repository.find_by_id(1)
            session['user'] = user.serialize()
            bp_order_report = BpOrderReport(project_detail)
        self.bp_order_report = bp_order_report

    def tearDown(self):
        super(BpOrderReportTests, self).tearDown()

    def test_get_payment_detail_text(self):
        # set_up
        engineer_history = EngineerHistory(
            engineer_id=1,
            payment_start_day=date(2017, 1, 1),
            payment_end_day=date(2017, 2, 28),
            payment_site=Site.twenty_five,
            payment_tax=Tax.eight,
            payment_per_month=100000,
            payment_rule=Rule.variable,
            payment_per_top_hour=1000,
            payment_per_bottom_hour=2000,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')

        expected = "test0 氏  ¥100,000.-/月額"\
            + "\n        "\
            + "超過単価：¥1,000.-/H  "\
            + "欠業単価：¥2,000.-/H"

        # テスト対象のメソッドを実行
        text = self.bp_order_report.get_payment_detail_text(engineer_history)
        self.assertEqual(text, expected)
