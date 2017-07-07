from datetime import datetime

from flask import session

from application import app
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.engineer_repository import EngineerRepository
from application.domain.repository.project_detail_repository import ProjectDetailRepository
from application.domain.repository.project_repository import ProjectRepository
from application.domain.repository.user_repository import UserRepository
from application.service.report.estimated_report import EstimatedReport
from tests import BaseTestCase


class EstimatedReportTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(EstimatedReportTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(EstimatedReportTests, cls).tearDownClass()

    def setUp(self):
        super(EstimatedReportTests, self).setUp()
        self.project_repository = ProjectRepository()
        self.user_repository = UserRepository()
        self.project_detail_repository = ProjectDetailRepository()
        self.engineer_repository = EngineerRepository()
        with app.test_request_context():
            project = self.project_repository.find_by_id(1)
            # 明細 = 作業
            project_detail_work = ProjectDetail(
                                        project_id=project.id,
                                        detail_type=DetailType.work,
                                        work_name='project_detail_work',
                                        billing_money=100000,
                                        created_at=datetime.today(),
                                        created_user='test',
                                        updated_at=datetime.today(),
                                        updated_user='test')
            project.project_details.append(project_detail_work)
            user = self.user_repository.find_by_id(1)
            session['user'] = user.serialize()
            estimated_report = EstimatedReport(project)
        self.estimated_report = estimated_report

    def tearDown(self):
        super(EstimatedReportTests, self).tearDown()

    def test_write_estimated_content_rows_if_blanket(self):
        # set_up
        self.estimated_report.project.contract_form = Contract.blanket

        # テスト対象のメソッドを実行
        self.estimated_report.write_estimated_content_rows()

        # 指定のセルに値が入っていることを確認。
        self.assertEqual(self.estimated_report.ws.get_named_range("estimation_no")[0].value,
                         self.estimated_report.project.estimation_no)
        self.assertIsNotNone(self.estimated_report.ws.get_named_range("printed_date")[0].value)
        self.assertEqual(self.estimated_report.ws.get_named_range("client_company_name")[0].value,
                         self.estimated_report.project.client_company.company_name)
        self.assertEqual(self.estimated_report.ws.get_named_range("project_name")[0].value,
                         self.estimated_report.project.project_name)
        self.assertEqual(self.estimated_report.ws.get_named_range("start_date")[0].value.date(),
                         self.estimated_report.project.start_date)
        self.assertEqual(self.estimated_report.ws.get_named_range("end_date")[0].value.date(),
                         self.estimated_report.project.end_date)
        self.assertEqual(self.estimated_report.ws.get_named_range("billing_timing")[0].value,
                         self.estimated_report.project.billing_timing.name_for_report)
        self.assertEqual(self.estimated_report.ws.get_named_range("contract_form")[0].value,
                         self.estimated_report.project.contract_form.name)

    def test_write_estimated_content_rows_if_not_blanket(self):
        # set_up
        self.estimated_report.project.contract_form = Contract.time_and_material

        # テスト対象のメソッドを実行
        self.estimated_report.write_estimated_content_rows()

        # 指定のセルに値が入っていることを確認。
        self.assertEqual(self.estimated_report.ws.get_named_range("estimation_no")[0].value,
                         self.estimated_report.project.estimation_no)
        self.assertIsNotNone(self.estimated_report.ws.get_named_range("printed_date")[0].value)
        self.assertEqual(self.estimated_report.ws.get_named_range("client_company_name")[0].value,
                         self.estimated_report.project.client_company.company_name)
        self.assertEqual(self.estimated_report.ws.get_named_range("project_name")[0].value,
                         self.estimated_report.project.project_name)
        self.assertEqual(self.estimated_report.ws.get_named_range("start_date")[0].value.date(),
                         self.estimated_report.project.start_date)
        self.assertEqual(self.estimated_report.ws.get_named_range("end_date")[0].value.date(),
                         self.estimated_report.project.end_date)
        self.assertEqual(self.estimated_report.ws.get_named_range("billing_timing")[0].value,
                         self.estimated_report.project.billing_timing.name_for_report)
        self.assertEqual(self.estimated_report.ws.get_named_range("contract_form")[0].value,
                         self.estimated_report.project.contract_form.name)

    def test_create_project_detail_rows_if_project_details_over_3(self):
        # テスト対象のメソッドを実行
        self.estimated_report.create_project_detail_rows()

        # プロジェクト明細が指定のセルに値が入っていることを確認（※1行のみ）。
        self.assertEqual(self.estimated_report.ws['B24'].value, 1)
        self.assertEqual(self.estimated_report.ws['C24'].value,
                         self.estimated_report.project.project_details[0].engineer.engineer_name)
        self.assertEqual(self.estimated_report.ws['G24'].value,
                         self.estimated_report.project.project_details[0].billing_money)
        self.assertEqual(self.estimated_report.ws['H24'].value,
                         self.estimated_report.project.project_details[0].remarks)
        # 消費税が指定のセルに値が入っていることを確認。
        self.assertEqual(self.estimated_report.ws['C30'].value, '消費税（なし）')
        self.assertEqual(self.estimated_report.ws['G30'].value,
                         self.estimated_report.project.tax_of_estimated_total_amount())
        # 合計が指定のセルに値が入っていることを確認。
        self.assertEqual(self.estimated_report.ws['C31'].value, '合計')
        self.assertEqual(self.estimated_report.ws['G31'].value,
                         self.estimated_report.project.estimated_total_amount
                         + self.estimated_report.project.tax_of_estimated_total_amount())

    def test_create_project_detail_rows_if_project_details_below_2(self):
        # set_up
        project = self.project_repository.find_by_id(2)
        project_detail = self.project_detail_repository.find_all()[1]
        project.project_details.append(project_detail)
        self.estimated_report.project = project

        # テスト対象のメソッドを実行
        self.estimated_report.create_project_detail_rows()

        # プロジェクト明細が指定のセルに値が入っていることを確認（※1行のみ）。
        self.assertEqual(self.estimated_report.ws['B24'].value, 1)
        self.assertEqual(self.estimated_report.ws['C24'].value,
                         self.estimated_report.project.project_details[0].engineer.engineer_name)
        self.assertEqual(self.estimated_report.ws['G24'].value,
                         self.estimated_report.project.project_details[0].billing_money)
        self.assertEqual(self.estimated_report.ws['H24'].value,
                         self.estimated_report.project.project_details[0].remarks)
        # 消費税が指定のセルに値が入っていることを確認。
        self.assertEqual(self.estimated_report.ws['C25'].value, '消費税（なし）')
        self.assertEqual(self.estimated_report.ws['G25'].value,
                         self.estimated_report.project.tax_of_estimated_total_amount())
        # 合計が指定のセルに値が入っていることを確認。
        self.assertEqual(self.estimated_report.ws['C26'].value, '合計')
        self.assertEqual(self.estimated_report.ws['G26'].value,
                         self.estimated_report.project.estimated_total_amount
                         + self.estimated_report.project.tax_of_estimated_total_amount())

    def test_create_contract_content_rows(self):
        # テスト対象のメソッドを実行
        self.estimated_report.current_row = 32
        self.estimated_report.create_contract_content_rows()

        # 指定のセルに値が入っていることを確認。
        self.assertEqual(self.estimated_report.ws['B32'].value, '作業内容')
        self.assertEqual(self.estimated_report.ws['E32'].value, self.estimated_report.project.contents)
        self.assertEqual(self.estimated_report.ws['B33'].value, '納品物')
        self.assertEqual(self.estimated_report.ws['E33'].value, self.estimated_report.project.deliverables)
        self.assertEqual(self.estimated_report.ws['B34'].value, '作業場所')
        self.assertEqual(self.estimated_report.ws['E34'].value, self.estimated_report.project.working_place)
        self.assertEqual(self.estimated_report.ws['B35'].value, '検査完了日')
        self.assertEqual(self.estimated_report.ws['E35'].value, self.estimated_report.project.inspection_date)
        self.assertEqual(self.estimated_report.ws['B36'].value, '作業責任者')
        self.assertEqual(self.estimated_report.ws['E36'].value, self.estimated_report.project.responsible_person)
        self.assertEqual(self.estimated_report.ws['B37'].value, '品質管理担当者')
        self.assertEqual(self.estimated_report.ws['E37'].value, self.estimated_report.project.quality_control)
        self.assertEqual(self.estimated_report.ws['B38'].value, '再委託先')
        self.assertEqual(self.estimated_report.ws['E38'].value, self.estimated_report.project.subcontractor)
        self.assertEqual(self.estimated_report.ws['B39'].value, '備考')
        self.assertEqual(self.estimated_report.ws['E39'].value, self.estimated_report.project.remarks)

    def test_create_contract_content_rows_if_billing_by_month(self):
        # set_up
        project = self.project_repository.find_by_id(2)
        project_detail = self.project_detail_repository.find_all()[1]
        project.project_details.append(project_detail)
        self.estimated_report.project = project

        # テスト対象のメソッドを実行
        self.estimated_report.current_row = 32
        self.estimated_report.create_contract_content_rows()

        # 指定のセルに値が入っていることを確認。
        self.assertEqual(self.estimated_report.ws['B32'].value, '作業内容')
        self.assertEqual(self.estimated_report.ws['E32'].value, self.estimated_report.project.contents)
        self.assertEqual(self.estimated_report.ws['B33'].value, '納品物')
        self.assertEqual(self.estimated_report.ws['E33'].value, self.estimated_report.project.deliverables)
        self.assertEqual(self.estimated_report.ws['B34'].value, '作業場所')
        self.assertEqual(self.estimated_report.ws['E34'].value, self.estimated_report.project.working_place)
        self.assertEqual(self.estimated_report.ws['B35'].value, '検査完了日')
        self.assertEqual(self.estimated_report.ws['E35'].value, '毎月月末')
        self.assertEqual(self.estimated_report.ws['B36'].value, '作業責任者')
        self.assertEqual(self.estimated_report.ws['E36'].value, self.estimated_report.project.responsible_person)
        self.assertEqual(self.estimated_report.ws['B37'].value, '品質管理担当者')
        self.assertEqual(self.estimated_report.ws['E37'].value, self.estimated_report.project.quality_control)
        self.assertEqual(self.estimated_report.ws['B38'].value, '再委託先')
        self.assertEqual(self.estimated_report.ws['E38'].value, self.estimated_report.project.subcontractor)
        self.assertEqual(self.estimated_report.ws['B39'].value, '備考')
        self.assertEqual(self.estimated_report.ws['E39'].value, self.estimated_report.project.remarks)
