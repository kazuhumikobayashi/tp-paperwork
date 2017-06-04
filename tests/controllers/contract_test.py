from datetime import date
from nose.tools import ok_

from application.domain.model.immutables.tax import Tax
from tests import BaseTestCase

from application.domain.repository.project_repository import ProjectRepository


class ContractTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ContractTests, cls).setUpClass()

    def setUp(self):
        super(ContractTests, self).setUp()
        self.project_repository = ProjectRepository()

    def tearDown(self):
        super(ContractTests, self).tearDown()

    # 契約画面に遷移する。
    def test_get_contract(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project = self.project_repository.find_all()[0]

        result = self.app.get('/contract/' + str(project.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないプロジェクトの場合はnot_found
    def test_get_contract_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/contract/0')
        self.assertEqual(result.status_code, 404)

    # 契約情報を保存できる
    def test_save_contract(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project = self.project_repository.find_all()[0]

        expected = '単体テスト_変更'
        project_id = project.id

        result = self.app.post('/contract/' + str(project_id), data={
            'project_name': expected,
            'project_name_for_bp': project.project_name_for_bp,
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'sales_person': project.sales_person,
            'estimation_no': project.estimation_no,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d'),
            'payment_tax': Tax.eight,
            'scope': project.scope,
            'contents': project.contents,
            'working_place': project.working_place,
            'delivery_place': project.delivery_place,
            'deliverables': project.deliverables,
            'inspection_date': project.inspection_date,
            'responsible_person': project.responsible_person,
            'quality_control': project.quality_control,
            'subcontractor': project.subcontractor,
            'remarks': project.remarks
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/contract/' + str(project.id) in result.headers['Location'])

        project = self.project_repository.find_by_id(project_id)
        actual = project.project_name
        self.assertEqual(actual, expected)

    # 同じ見積もりNoは登録できない
    def test_duplicate_estimate_no(self):

        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/project/create', data={
            'project_name': '重複テスト',
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31'
        })
        self.assertEqual(result.status_code, 302)
        project_id = result.headers['Location'][-1:]
        project = self.project_repository.find_by_id(project_id)

        duplicate_estimation_no = 'duplicate_estimation_no'
        result = self.app.post('/contract/' + str(project_id), data={
            'project_name': 'project_name',
            'project_name_for_bp': project.project_name_for_bp,
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'sales_person': project.sales_person,
            'estimation_no': duplicate_estimation_no,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d'),
            'payment_tax': Tax.eight,
            'scope': project.scope,
            'contents': project.contents,
            'working_place': project.working_place,
            'delivery_place': project.delivery_place,
            'deliverables': project.deliverables,
            'inspection_date': project.inspection_date,
            'responsible_person': project.responsible_person,
            'quality_control': project.quality_control,
            'subcontractor': project.subcontractor,
            'remarks': project.remarks
        })
        self.assertEqual(result.status_code, 302)

        result = self.app.post('/project/create', data={
            'project_name': '重複テスト',
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31'
        })
        self.assertEqual(result.status_code, 302)
        project_id = result.headers['Location'][-1:]
        project = self.project_repository.find_by_id(project_id)

        result = self.app.post('/contract/' + str(project_id), data={
            'project_name': 'project_name',
            'project_name_for_bp': project.project_name_for_bp,
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'sales_person': project.sales_person,
            'estimation_no': duplicate_estimation_no,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d'),
            'payment_tax': Tax.eight,
            'scope': project.scope,
            'contents': project.contents,
            'working_place': project.working_place,
            'delivery_place': project.delivery_place,
            'deliverables': project.deliverables,
            'inspection_date': project.inspection_date,
            'responsible_person': project.responsible_person,
            'quality_control': project.quality_control,
            'subcontractor': project.subcontractor,
            'remarks': project.remarks
        })

        # 保存できないことを確認
        self.assertEqual(result.status_code, 200)

    # 次の期の契約情報を保存できる
    def test_save_contract_second_basic(self):
        project = self.project_repository.find_all()[0]

        result = self.app.post('/contract/' + str(project.id), data={
            'project_name': project.project_name,
            'project_name_for_bp': project.project_name_for_bp,
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'sales_person': project.sales_person,
            'estimation_no': project.estimation_no,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': str(int(project.start_date.strftime('%Y')) + 1) + '/4/1',
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d'),
            'payment_tax': Tax.eight,
            'scope': project.scope,
            'contents': project.contents,
            'working_place': project.working_place,
            'delivery_place': project.delivery_place,
            'deliverables': project.deliverables,
            'inspection_date': project.inspection_date,
            'responsible_person': project.responsible_person,
            'quality_control': project.quality_control,
            'subcontractor': project.subcontractor,
            'remarks': project.remarks
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/contract/' + str(project.id) in result.headers['Location'])

    # 10月以降の契約情報を保存できる
    def test_save_contract_october(self):
        project = self.project_repository.find_all()[0]

        result = self.app.post('/contract/' + str(project.id), data={
            'project_name': project.project_name,
            'project_name_for_bp': project.project_name_for_bp,
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'sales_person': project.sales_person,
            'estimation_no': project.estimation_no,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': str(int(project.start_date.strftime('%Y')) + 1) + '/10/1',
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d'),
            'payment_tax': Tax.eight,
            'scope': project.scope,
            'contents': project.contents,
            'working_place': project.working_place,
            'delivery_place': project.delivery_place,
            'deliverables': project.deliverables,
            'inspection_date': project.inspection_date,
            'responsible_person': project.responsible_person,
            'quality_control': project.quality_control,
            'subcontractor': project.subcontractor,
            'remarks': project.remarks
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/contract/' + str(project.id) in result.headers['Location'])
