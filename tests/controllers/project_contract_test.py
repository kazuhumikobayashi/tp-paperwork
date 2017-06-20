from datetime import date, datetime
from nose.tools import ok_

from application import db
from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.engineer import Engineer
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.fraction import Fraction
from application.domain.model.immutables.holiday_flag import HolidayFlag
from application.domain.model.immutables.round import Round
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.status import Status
from application.domain.model.immutables.tax import Tax
from application.domain.model.project import Project
from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.project_detail_repository import ProjectDetailRepository
from tests import BaseTestCase

from application.domain.repository.project_repository import ProjectRepository


class ProjectContractTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectContractTests, cls).setUpClass()

    def setUp(self):
        super(ProjectContractTests, self).setUp()
        self.project_repository = ProjectRepository()
        self.project_detail_repository = ProjectDetailRepository()

    def tearDown(self):
        super(ProjectContractTests, self).tearDown()

    # 契約画面に遷移する。
    def test_get_contract(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project = self.project_repository.find_all()[0]

        result = self.app.get('/project/contract/' + str(project.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないプロジェクトの場合はnot_found
    def test_get_contract_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/contract/0')
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

        result = self.app.post('/project/contract/' + str(project_id), data={
            'project_name': expected,
            'project_name_for_bp': project.project_name_for_bp,
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'sales_person': project.sales_person,
            'estimation_no': project.estimation_no,
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d'),
            'billing_tax': Tax.eight,
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
        ok_('/project/contract/' + str(project.id) in result.headers['Location'])

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
        project_id = result.headers['Location'].split('/')[-1]
        project = self.project_repository.find_by_id(project_id)

        duplicate_estimation_no = 'duplicate_estimation_no'
        result = self.app.post('/project/contract/' + str(project_id), data={
            'project_name': 'project_name',
            'project_name_for_bp': project.project_name_for_bp,
            'status': project.status,
            'recorded_department_id': '1',
            'sales_person': project.sales_person,
            'estimation_no': duplicate_estimation_no,
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket,
            'billing_timing': BillingTiming.billing_at_last,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': date.today().strftime('%Y/%m/%d'),
            'billing_tax': Tax.eight,
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
        project_id = result.headers['Location'].split('/')[-1]
        project = self.project_repository.find_by_id(project_id)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'project_name': 'project_name',
            'project_name_for_bp': project.project_name_for_bp,
            'status': project.status,
            'recorded_department_id': '1',
            'sales_person': project.sales_person,
            'estimation_no': duplicate_estimation_no,
            'end_user_company_id': '1',
            'client_company_id': '1',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket,
            'billing_timing': BillingTiming.billing_at_last,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': date.today().strftime('%Y/%m/%d'),
            'billing_tax': Tax.eight,
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

        result = self.app.post('/project/contract/' + str(project.id), data={
            'project_name': project.project_name,
            'project_name_for_bp': project.project_name_for_bp,
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'sales_person': project.sales_person,
            'estimation_no': project.estimation_no,
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': str(int(project.start_date.strftime('%Y')) + 1) + '/4/1',
            'end_date': str(int(project.start_date.strftime('%Y')) + 1) + '/6/30',
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d'),
            'billing_tax': Tax.eight,
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
        ok_('/project/contract/' + str(project.id) in result.headers['Location'])

    # 10月以降の契約情報を保存できる
    def test_save_contract_october(self):
        project = self.project_repository.find_all()[10]
        project.project_details.append(self.project_detail_repository.find_by_id(3))

        result = self.app.post('/project/contract/' + str(project.id), data={
            'project_name': project.project_name,
            'project_name_for_bp': project.project_name_for_bp,
            'status': Status.done,
            'recorded_department_id': project.recorded_department_id,
            'sales_person': project.sales_person,
            'estimation_no': project.estimation_no,
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': str(int(project.start_date.strftime('%Y')) + 1) + '/10/1',
            'end_date': str(int(project.start_date.strftime('%Y')) + 1) + '/12/31',
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
            'estimated_total_amount': project.estimated_total_amount,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d'),
            'billing_tax': Tax.eight,
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
        ok_('/project/contract/' + str(project.id) in result.headers['Location'])

    # 計上部署は必須
    def test_required_recorded_department(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            status=Status.start,
            recorded_department_id=1,
            estimation_no='M0001',
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date='2016/1/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        before = project.recorded_department_id

        # 計上部署が空だと更新できないことを確認
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': project.status,
            'recorded_department_id': '',
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing
        })
        self.assertEqual(result.status_code, 200)

        # 計上部署の値が変わっていないことを確認。
        after = project.recorded_department_id
        self.assertEqual(before, after)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 見積番号は必須
    def test_required_estimation_no(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            status=Status.start,
            recorded_department_id=1,
            estimation_no='M0002',
            project_name='validation_test',
            end_user_company_id='4',
            client_company_id='3',
            start_date='2016/1/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        before = project.estimation_no

        # 見積番号が空だと更新できないことを確認
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': '',
            'project_name': project.project_name,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
        })
        self.assertEqual(result.status_code, 200)

        # 見積番号の値が変わっていないことを確認。
        after = project.estimation_no
        self.assertEqual(before, after)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # プロジェクト名は必須
    def test_required_project_name(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            status=Status.start,
            recorded_department_id=1,
            estimation_no='M0003',
            project_name='validation_test',
            end_user_company_id='4',
            client_company_id='3',
            start_date='2016/1/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        before = project.project_name

        # プロジェクト名が空だと更新できないことを確認
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': '',
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
        })
        self.assertEqual(result.status_code, 200)

        # プロジェクト名の値が変わっていないことを確認。
        after = project.project_name
        self.assertEqual(before, after)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # エンドユーザーは必須
    def test_required_end_user_company(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            status=Status.start,
            recorded_department_id=1,
            estimation_no='M0004',
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date='2016/1/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        before = project.end_user_company_id

        # エンドユーザーが空だと更新できないことを確認
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': '',
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
        })
        self.assertEqual(result.status_code, 200)

        # エンドユーザーの値が変わっていないことを確認。
        after = project.end_user_company_id
        self.assertEqual(before, after)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 顧客は必須
    def test_required_client_company(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            status=Status.start,
            recorded_department_id=1,
            estimation_no='M0005',
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date='2016/1/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        before = project.client_company_id

        # 顧客が空だと更新できないことを確認
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': '',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
        })
        self.assertEqual(result.status_code, 200)

        # 顧客の値が変わっていないことを確認。
        after = project.client_company_id
        self.assertEqual(before, after)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # プロジェクト開始年月日は必須
    def test_required_start_day(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            status=Status.start,
            recorded_department_id=1,
            estimation_no='M0006',
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date='2016/1/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        before = project.start_date

        # 開始年月日が空だと更新できないことを確認
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': '',
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
        })
        self.assertEqual(result.status_code, 200)

        # 開始年月日の値が変わっていないことを確認。
        after = project.start_date
        self.assertEqual(before, after)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # プロジェクト終了年月日は必須
    def test_required_end_day(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            status=Status.start,
            recorded_department_id=1,
            estimation_no='M0007',
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date='2016/1/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        before = project.end_date

        # 終了年月日が空だと更新できないことを確認
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': '',
            'contract_form': project.contract_form,
            'billing_timing': project.billing_timing,
        })
        self.assertEqual(result.status_code, 200)

        # 終了年月日の値が変わっていないことを確認。
        after = project.end_date
        self.assertEqual(before, after)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 契約形態は必須
    def test_required_contract_form(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            status=Status.start,
            recorded_department_id=1,
            estimation_no='M0008',
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date='2016/1/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        before = project.contract_form

        # 契約形態が空だと更新できないことを確認
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': '',
            'billing_timing': project.billing_timing,
        })
        self.assertEqual(result.status_code, 200)

        # 契約形態の値が変わっていないことを確認。
        after = project.contract_form
        self.assertEqual(before, after)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 請求タイミングは必須
    def test_required_billing_timing(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            status=Status.start,
            recorded_department_id=1,
            estimation_no='M0009',
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date='2016/1/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        before = project.billing_timing

        # 契約形態が空だと更新できないことを確認
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': project.status,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': project.end_user_company_id,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form,
            'billing_timing': 'test',
        })
        self.assertEqual(result.status_code, 200)

        # 請求タイミングの値が変わっていないことを確認。
        after = project.billing_timing
        self.assertEqual(before, after)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日を計算（支払いサイト25）
    def test_get_deposit_date_by_site_25(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.twenty_five
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが25のため、deposit_dateには、end_dateの翌月25日（2017/1/25）が入る。
        expected = date(2017, 1, 25)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0010',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2017/1/25 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日を計算（支払いサイト30）
    def test_get_deposit_date_by_site_30(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.thirty
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが30のため、deposit_dateには、end_dateの翌月末日（2017/1/31）が入る。
        expected = date(2017, 1, 31)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0011',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2017/1/31 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日を計算（支払いサイト40）
    def test_get_deposit_date_by_site_40(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.forty
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが40のため、deposit_dateには、end_dateの翌々月10日（2017/2/10）が入る。
        expected = date(2017, 2, 10)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0012',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2017/2/10 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日を計算（支払いサイト50）
    def test_get_deposit_date_by_site_50(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.fifty
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが50のため、deposit_dateには、end_dateの翌々月20日（2017/2/20）が入る。
        expected = date(2017, 2, 20)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0013',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2017/2/20 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日を計算（支払いサイト51）
    def test_get_deposit_date_by_site_51(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.fifty_one
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが51のため、deposit_dateには、end_dateの翌々月21日（2017/2/21）が入る。
        expected = date(2017, 2, 21)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0014',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2017/2/21 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日を計算（支払いサイト55）
    def test_get_deposit_date_by_site_55(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.fifty_five
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが55のため、deposit_dateには、end_dateの翌々月25日（2017/2/25）が入るが、
        # 25日は土曜日なので、1日前倒しして24日（2017/2/24）が入る。
        expected = date(2017, 2, 24)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0015',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2017/2/24 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日を計算（支払いサイト60）
    def test_get_deposit_date_by_site_60(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.sixty
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが60のため、deposit_dateには、end_dateの翌々月末日（2017/2/28）が入る。
        expected = date(2017, 2, 28)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0016',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2017/2/28 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日が土曜の場合、前倒しして先週の金曜日にする
    def test_before_deposit_date_if_saturday(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 7, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.forty
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが40のため、deposit_dateには、end_dateの翌々月末日（2016/9/10）が入るが、
        # 2016/9/10は土曜日のため、前倒しして2017/9/9が入る。
        expected = date(2016, 9, 9)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0017',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2017/9/8 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日が土曜の場合、後ろ倒しして先週の金曜日にする
    def test_after_deposit_date_if_saturday(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 7, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.forty
        project.client_company.bank_holiday_flag = HolidayFlag.after

        # 支払いサイトが40のため、deposit_dateには、end_dateの翌々月末日（2016/9/10）が入るが、
        # 2016/9/10は土曜日のため、後ろ倒ししてして2017/9/12が入る。
        expected = date(2016, 9, 12)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0018',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2017/9/12 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日が日曜日の場合、前倒しして先週の金曜日にする
    def test_before_deposit_date_if_sunday(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 5, 30).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.forty
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが40のため、deposit_dateには、end_dateの翌々月10日（2016/7/10）が入るが、
        # 2016/7/10は日曜日のため、前倒しして2016/7/8が入る。
        expected = date(2016, 7, 8)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0019',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2016/7/8 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日が土曜の場合、後ろ倒しして先週の金曜日にする
    def test_after_deposit_date_if_sunday(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2016, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2016, 5, 30).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.forty
        project.client_company.bank_holiday_flag = HolidayFlag.after

        # 支払いサイトが40のため、deposit_dateには、end_dateの翌々月10日（2016/7/10）が入るが、
        # 2016/7/10は日曜日のため、後ろ倒ししてして2016/7/11が入る。
        expected = date(2016, 7, 11)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0020',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2016/7/11 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日が祝日の場合、前倒しする（祝日が月曜の場合）
    def test_before_deposit_date_if_holiday_monday(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2015, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2015, 10, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.fifty_one
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが51のため、deposit_dateには、end_dateの翌々月21日（2015/12/21）が入るが、
        # 2015/12/21は祝日（テストデータ）のため、前倒しして2015/12/18が入る（21日が月曜のため、先週の金曜になる）。
        expected = date(2015, 12, 18)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0021',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2016/12/18 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日が祝日の場合、後ろ倒しする（祝日が月曜の場合）
    def test_after_deposit_date_if_holiday_monday(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2015, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2015, 10, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.fifty_one
        project.client_company.bank_holiday_flag = HolidayFlag.after

        # 支払いサイトが51のため、deposit_dateには、end_dateの翌々月21日（2015/12/21）が入るが、
        # 2015/12/21は祝日（テストデータ）のため、後ろ倒しして2015/12/22が入る。
        expected = date(2015, 12, 22)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0022',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2016/12/22 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日が祝日の場合、前倒しする（祝日が金曜の場合）
    def test_before_deposit_date_if_holiday_friday(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2015, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2015, 10, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.fifty_five
        project.client_company.bank_holiday_flag = HolidayFlag.before

        # 支払いサイトが55のため、deposit_dateには、end_dateの翌々月25日（2015/12/25）が入るが、
        # 2015/12/25は祝日（テストデータ）のため、前倒しして2015/12/24が入る。
        expected = date(2015, 12, 24)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0023',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2016/12/24 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 支払い予定日が祝日の場合、後ろ倒しする（祝日が金曜の場合）
    def test_after_deposit_date_if_holiday_friday(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # プロジェクトを新規作成
        project = Project(
            project_name='validation_test',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2015, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2015, 10, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id
        project.client_company.billing_site = Site.fifty_five
        project.client_company.bank_holiday_flag = HolidayFlag.after

        # 支払いサイトが55のため、deposit_dateには、end_dateの翌々月25日（2015/12/25）が入るが、
        # 2015/12/25は祝日（テストデータ）のため、後ろ倒しして2015/12/28が入る（25日が金曜のため、来週の月曜28日となる）。
        expected = date(2015, 12, 28)

        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.start.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0024',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value,
            'deposit_date': ''
        })
        self.assertEqual(result.status_code, 302)

        # 2016/12/28 になっていることを確認
        actual = project.deposit_date
        self.assertEqual(actual, expected)

        # プロジェクトを削除
        db.session.delete(project)
        db.session.commit()

    # 明細がengineer（bpの場合）の場合、ステータスを契約完了にして更新すると
    # engineerの請求開始年月～請求終了年月の実績レコードが作成される。
    def test_create_bp_engineer_result_when_status_done(self):
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        project = Project(
            project_name='test_copy_project',
            project_name_for_bp='copy_project',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='M0001-11',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2017, 1, 1),
            end_date=date(2017, 12, 31),
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            deposit_date='20/12/31',
            scope='test',
            contents=None,
            working_place=None,
            delivery_place=None,
            deliverables=None,
            inspection_date=None,
            responsible_person=None,
            quality_control=None,
            subcontractor=None,
            remarks=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        engineer = Engineer(
            engineer_name='エンジニア',
            company_id=2,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': engineer.id,
            'billing_money': '100000000',
            'billing_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'billing_end_day': date(2017, 3, 1).strftime('%Y/%m'),
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed.value,
            'billing_fraction_rule': '',
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])
        project_detail_id = result.headers['Location'].split('/')[-1]

        result = self.app.post('/project/contract/' + str(project.id), data={
            'status': Status.done.value,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': str(project.end_user_company_id),
            'client_company_id': str(project.client_company_id),
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form.value,
            'billing_timing': project.billing_timing.value,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d')
        })
        self.assertEqual(result.status_code, 302)
        ok_('/contract' in result.headers['Location'])

        project_detail = self.project_detail_repository.find_by_id(project_detail_id)
        # 明細（project_detail）の請求契約期間が2017年の1～3月のため、1～3月分の実績レコードが作成される。
        expected_1 = date(2017, 1, 1)
        expected_2 = date(2017, 2, 1)
        expected_3 = date(2017, 3, 1)
        actual_1 = project_detail.project_results[0].result_month
        actual_2 = project_detail.project_results[1].result_month
        actual_3 = project_detail.project_results[2].result_month

        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)
        self.assertEqual(actual_3, expected_3)

        # tear_down
        self.app.get('/project/contract/delete/' + str(project_detail.id))
        self.app.get('/project/delete/' + str(project.id))

    # 明細がengineer（bp以外）の場合、ステータスを契約完了にして更新すると
    # engineerの請求開始年月～請求終了年月の実績レコードが作成される。
    def test_create_engineer_result_except_bp_when_status_done(self):
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        project = Project(
            project_name='test_copy_project',
            project_name_for_bp='copy_project',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='M0001-11',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2017, 1, 1),
            end_date=date(2017, 12, 31),
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            deposit_date='20/12/31',
            scope='test',
            contents=None,
            working_place=None,
            delivery_place=None,
            deliverables=None,
            inspection_date=None,
            responsible_person=None,
            quality_control=None,
            subcontractor=None,
            remarks=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        engineer = Engineer(
            engineer_name='エンジニア',
            company_id=4,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': engineer.id,
            'billing_money': '100000000',
            'billing_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'billing_end_day': date(2017, 3, 1).strftime('%Y/%m'),
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed.value,
            'billing_fraction_rule': ''
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])
        project_detail_id = result.headers['Location'].split('/')[-1]

        result = self.app.post('/project/contract/' + str(project.id), data={
            'status': Status.done.value,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': str(project.end_user_company_id),
            'client_company_id': str(project.client_company_id),
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form.value,
            'billing_timing': project.billing_timing.value,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d')
        })
        self.assertEqual(result.status_code, 302)
        ok_('/contract' in result.headers['Location'])

        project_detail = self.project_detail_repository.find_by_id(project_detail_id)
        # bpでないので、支払予定日がNoneであることを確認する。
        expected_1 = date(2017, 1, 1)
        expected_2 = date(2017, 2, 1)
        expected_3 = date(2017, 3, 1)
        actual_1 = project_detail.project_results[0].result_month
        actual_2 = project_detail.project_results[1].result_month
        actual_3 = project_detail.project_results[2].result_month

        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)
        self.assertEqual(actual_3, expected_3)

        # tear_down
        self.app.get('/project/contract/delete/' + str(project_detail.id))
        self.app.get('/project/delete/' + str(project.id))

    # 明細がworkの場合、ステータスを契約完了にして更新すると
    # プロジェクト開始～終了年月の請求レコードが作成される。
    def test_update_work_billing_when_status_done(self):
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        project = self.project_repository.find_by_id(6)

        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.work.value,
            'work_name': 'test',
            'billing_money': '100000000',
            'engineer_id': '',
            'billing_fraction_rule': ''
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])
        project_detail_id = result.headers['Location'].split('/')[-1]

        result = self.app.post('/project/contract/' + str(project.id), data={
            'status': Status.done.value,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': date(2017, 1, 1).strftime('%Y/%m/%d'),
            'end_date': date(2017, 3, 31).strftime('%Y/%m/%d'),
            'contract_form': project.contract_form.value,
            'billing_timing': project.billing_timing.value,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d')
        })
        self.assertEqual(result.status_code, 302)
        ok_('/contract' in result.headers['Location'])

        project_detail = self.project_detail_repository.find_by_id(project_detail_id)
        # プロジェクト期間が2017年の1～3月のため、1～3月分の実績レコードが作成される。
        expected_1 = date(2017, 1, 1)
        expected_2 = date(2017, 2, 1)
        expected_3 = date(2017, 3, 1)
        actual_1 = project_detail.project_billings[0].billing_month
        actual_2 = project_detail.project_billings[1].billing_month
        actual_3 = project_detail.project_billings[2].billing_month

        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)
        self.assertEqual(actual_3, expected_3)

        # tear_down
        self.app.get('/project/contract/delete/' + str(project_detail.id))
        self.app.get('/project/delete/' + str(project.id))

    # プロジェクト明細画面に遷移する。
    def test_get_project_detail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project_detail = self.project_detail_repository.find_all()[0]

        result = self.app.get('/project/contract/detail/' + str(project_detail.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないプロジェクト明細画面には遷移できない。
    def test_get_project_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/contract/detail/0')
        self.assertEqual(result.status_code, 404)

    # プロジェクト明細登録画面に遷移する。
    def test_get_project_detail_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        result = self.app.get('/project/contract/create?project_id=' + str(project.id))
        self.assertEqual(result.status_code, 200)

    # プロジェクト明細を作業で新規登録できることを確認。
    def test_create_project_detail_by_work(self):
        before = len(self.project_detail_repository.find_all())
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # プロジェクトが保存できることを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.work,
            'work_name': '作業',
            'billing_money': '100000',
            'engineer_id': '',
            'billing_fraction_rule': '',
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])

        # 件数が増えていることを確認。
        after = len(self.project_detail_repository.find_all())
        # 件数が1件増えていることを確認
        self.assertEqual(before+1, after)

    # プロジェクト明細を技術者で新規登録できることを確認。
    def test_create_project_detail_by_engineer(self):
        before = len(self.project_detail_repository.find_all())
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        project = Project(
                    status=Status.done,
                    recorded_department_id=1,
                    estimation_no='M0001',
                    project_name='validation_test',
                    end_user_company_id=4,
                    client_company_id=3, start_date='2016/1/1',
                    end_date='2016/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')
        db.session.add(project)
        db.session.commit()

        # プロジェクトが保存できることを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '3',
            'billing_money': '100000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': 100,
            'billing_top_base_hour': 200,
            'billing_free_base_hour': '1/100, 1/200',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': Fraction.thousand.value,
            'billing_fraction_rule': Round.down.value,
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])

        # 件数が増えていることを確認。
        after = len(self.project_detail_repository.find_all())
        # 件数が1件増えていることを確認
        self.assertEqual(before+1, after)

        # teardown
        db.session.delete(project)
        db.session.commit()

    # プロジェクト明細を削除できる
    def test_delete_project_detail(self):
        # 削除用のプロジェクトを登録
        project_detail = ProjectDetail(
            project_id=1,
            detail_type=DetailType.work,
            work_name='delete_project_detail_test',
            billing_money='100000',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project_detail)
        db.session.commit()

        delete_project_detail_id = project_detail.id
        project_id = project_detail.project.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        project_detail = self.project_detail_repository.find_by_id(delete_project_detail_id)

        result = self.app.get('/project/contract/delete/' + str(project_detail.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/contract/' + str(project_id) in result.headers['Location'])

        # 削除したプロジェクトが存在しないことを確認
        project_detail = self.project_detail_repository.find_by_id(delete_project_detail_id)
        self.assertIsNone(project_detail.id)

    # 存在しないプロジェクト明細は削除できない
    def test_delete_project_detail_fail(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/contract/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project' in result.headers['Location'])

        after = len(self.project_detail_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    def test_required_work_name_if_work(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 作業名が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.work,
            'work_name': '',
            'billing_money': '100000',
            'engineer_id': '',
            'billing_fraction_rule': ''
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_money_if_work(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求金額が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.work,
            'work_name': 'test_project_detail',
            'billing_money': '',
            'engineer_id': '',
            'billing_fraction_rule': ''
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_engineer_id_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 技術者が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '',
            'billing_money': '100000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_money_id_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求金額が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_start_day_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求開始年月が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_end_day_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求終了年月が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_per_month_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_rule_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': '',
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_bottom_base_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求フリー入力時間が空の場合、請求下限時間が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '',
            'billing_top_base_hour': '200',
            'billing_free_base_hour': '',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': Fraction.thousand.value,
            'billing_fraction_rule': Round.down.value,

        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_top_base_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求フリー入力時間が空の場合、請求上限時間が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '100',
            'billing_top_base_hour': '',
            'billing_free_base_hour': '',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': Fraction.thousand.value,
            'billing_fraction_rule': Round.down.value
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_free_base_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求下限・上限時間が空の場合、請求フリー入力時間が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '',
            'billing_top_base_hour': '',
            'billing_free_base_hour': '',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': Fraction.thousand.value,
            'billing_fraction_rule': Round.down.value
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_per_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求時間単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '100',
            'billing_top_base_hour': '200',
            'billing_free_base_hour': '1/100、1/200',
            'billing_per_hour': '',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': Fraction.thousand.value,
            'billing_fraction_rule': Round.down.value

        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_per_bottom_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求△下限時間単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '100',
            'billing_top_base_hour': '200',
            'billing_free_base_hour': '1/100、1/200',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '',
            'billing_per_top_hour': '1000',
            'billing_fraction': Fraction.thousand.value,
            'billing_fraction_rule': Round.down.value
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_per_top_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求＋上限時間単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '100',
            'billing_top_base_hour': '200',
            'billing_free_base_hour': '1/100、1/200',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '',
            'billing_fraction': Fraction.thousand.value,
            'billing_fraction_rule': Round.down.value
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    # 支払い予定日を計算（支払いサイト30）
    def test_get_payment_date_by_site_30(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # set_up
        company = Company(
            company_name='会社',
            contract_date=datetime.today().strftime('%Y/%m/%d'),
            payment_site=Site.thirty,
            payment_tax=Tax.eight,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='エンジニア',
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        project = Project(
            project_name='プロジェクト',
            status=Status.done,
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2017, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2017, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': engineer.id,
            'billing_money': '1000000',
            'billing_start_day': '2017/3',
            'billing_end_day': '2017/4',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
            'billing_fraction_rule': ''
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])

        # 契約期間は3月～4月で支払いサイトが30のため、
        # 3月のpayment_dateには翌月末日（2017/4/30（日））だが月末は前倒しのため、2017/4/28（金曜）、
        # 4月のpayment_dateには翌月末日（2017/5/31（水））が入る。
        expected_in_march = date(2017, 4, 28)
        expected_in_april = date(2017, 5, 31)

        # 保存したproject_detailを取得
        project_detail_id = result.headers['Location'].split('/')[-1]
        project_detail = self.project_detail_repository.find_by_id(project_detail_id)

        # 3月のpayment_dateには、2017/4/28が入っていることを確認。
        actual_in_march = project_detail.project_results[0].payment_expected_date
        self.assertEqual(actual_in_march, expected_in_march)

        # 4月のpayment_dateには、2017/5/31が入っていることを確認。
        actual_in_april = project_detail.project_results[1].payment_expected_date
        self.assertEqual(actual_in_april, expected_in_april)

    # 支払い予定日を計算（支払いサイト50）
    def test_get_payment_date_by_site_50(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # set_up
        company = Company(
            company_name='会社',
            contract_date=datetime.today().strftime('%Y/%m/%d'),
            payment_site=Site.fifty,
            payment_tax=Tax.eight,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='エンジニア',
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        project = Project(
            project_name='プロジェクト',
            status=Status.done,
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2017, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2017, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': engineer.id,
            'billing_money': '1000000',
            'billing_start_day': '2017/3',
            'billing_end_day': '2017/4',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
            'billing_fraction_rule': ''
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])

        # 契約期間は3月～4月で支払いサイトが50のため、
        # 3月のpayment_dateには翌月末日（2017/5/20（土））だが月末以外後ろ倒しのため、2017/4/22（月）、
        # 4月のpayment_dateには翌月末日（2017/6/20（火））が入る。
        expected_in_march = date(2017, 5, 22)
        expected_in_april = date(2017, 6, 20)

        # 保存したproject_detailを取得
        project_detail_id = result.headers['Location'].split('/')[-1]
        project_detail = self.project_detail_repository.find_by_id(project_detail_id)

        # 3月のpayment_dateには、2017/4/28が入っていることを確認。
        actual_in_march = project_detail.project_results[0].payment_expected_date
        self.assertEqual(actual_in_march, expected_in_march)

        # 4月のpayment_dateには、2017/5/31が入っていることを確認。
        actual_in_april = project_detail.project_results[1].payment_expected_date
        self.assertEqual(actual_in_april, expected_in_april)

    # ステータスが契約完了になった後でworkの明細を新規登録した場合、
    # プロジェクト開始～終了年月の請求レコードが作成される。
    def test_create_work_billing_when_status_done(self):
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        project = self.project_repository.find_by_id(7)

        result = self.app.post('/project/contract/' + str(project.id), data={
            'status': Status.done.value,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': date(2017, 1, 1).strftime('%Y/%m/%d'),
            'end_date': date(2017, 3, 31).strftime('%Y/%m/%d'),
            'contract_form': project.contract_form.value,
            'billing_timing': project.billing_timing.value,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d')
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract' in result.headers['Location'])

        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.work.value,
            'work_name': 'test',
            'billing_money': '100000000',
            'engineer_id': '',
            'billing_fraction_rule': ''
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])
        project_detail_id = result.headers['Location'].split('/')[-1]

        project_detail = self.project_detail_repository.find_by_id(project_detail_id)
        # プロジェクト期間が2017年の1～3月のため、1～3月分の実績レコードが作成される。
        expected_1 = date(2017, 1, 1)
        expected_2 = date(2017, 2, 1)
        expected_3 = date(2017, 3, 1)
        actual_1 = project_detail.project_billings[0].billing_month
        actual_2 = project_detail.project_billings[1].billing_month
        actual_3 = project_detail.project_billings[2].billing_month

        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)
        self.assertEqual(actual_3, expected_3)

    # 開始日より終了日の方が小さい場合はエラー
    def test_start_date_less_than_end_date(self):
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        project = self.project_repository.find_by_id(7)
        before = str(project)

        result = self.app.post('/project/contract/' + str(project.id), data={
            'status': Status.done.value,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': date(2017, 4, 1).strftime('%Y/%m/%d'),
            'end_date': date(2017, 3, 31).strftime('%Y/%m/%d'),
            'contract_form': project.contract_form.value,
            'billing_timing': project.billing_timing.value,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d')
        })
        self.assertEqual(result.status_code, 200)

        # 更新されていないことを確認。
        after = str(self.project_repository.find_by_id(7))
        self.assertEqual(before, after)

    # 開始日より終了日の方が小さい場合はエラー
    def test_billing_start_date_less_than_billing_end_date(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '100000000',
            'billing_start_day': '2016/2',
            'billing_end_day': '2016/1',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)
