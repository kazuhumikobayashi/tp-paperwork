from urllib.parse import urlencode

from datetime import date, timedelta, datetime
from nose.tools import ok_

from application import db
from application.domain.model.estimation_remarks import EstimationRemarks
from application.domain.model.order_remarks import OrderRemarks
from application.domain.model.project import Project
from application.domain.repository.project_repository import ProjectRepository
from tests import BaseTestCase


class ProjectTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectTests, cls).setUpClass()

    def setUp(self):
        super(ProjectTests, self).setUp()
        self.project_repository = ProjectRepository()

    def tearDown(self):
        super(ProjectTests, self).tearDown()

    # プロジェクトの検索画面に遷移する。
    def test_get_project(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_project_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/page/2')
        self.assertEqual(result.status_code, 200)

    # プロジェクトを検索する。
    def test_search_project(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'start_date': "2016/1/1",
                                               'end_date': '2017/1/1',
                                               'project_name': 'test',
                                               'end_user': 'test',
                                               'client_company_id': '1',
                                               'recorded_department_id': '1'})
        result = self.app.get('/project/?' + query_string)

        self.assertEqual(result.status_code, 200)

    # プロジェクト登録画面に遷移する。
    def test_get_project_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/create')
        self.assertEqual(result.status_code, 200)

    # プロジェクト詳細画面に遷移する。
    def test_get_project_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project = self.project_repository.find_all()[0]

        result = self.app.get('/project/detail/' + str(project.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないプロジェクトの場合はnot_found
    def test_get_project_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/detail/0')
        self.assertEqual(result.status_code, 404)

    # プロジェクトの基本情報を保存できる
    def test_create_project_basic(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })

        result = self.app.post('/project/create', data={
            'project_name': 'test_create_project_basic',
            'end_user': 'test',
            'client_company_id': '1',
            'start_date': (datetime.today() + timedelta(days=1)).strftime('%Y/%m/%d'),
            'end_date': '2099/12/31',
            'recorded_department_id': '1',
            'over_time_calculation_id': '1',
            'contract_form_id': '1',
            'status_id': '1',
            'billing_timing': '1',
            'remarks': 'test',
            'save': 'basic'
        })
        # プロジェクトが保存できることを確認
        self.assertEqual(result.status_code, 302)

    # プロジェクトの基本情報を保存できる
    def test_save_project_basic(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project = self.project_repository.find_all()[0]

        expected = 'test_save_project_basic'
        project_id = project.id

        result = self.app.post('/project/detail/' + str(project_id), data={
            'project_name': expected,
            'end_user': 'test',
            'client_company_id': '1',
            'start_date': (datetime.today() + timedelta(days=1)).strftime('%Y/%m/%d'),
            'end_date': '2099/12/31',
            'recorded_department_id': '1',
            'over_time_calculation_id': '1',
            'contract_form_id': '1',
            'status_id': '1',
            'billing_timing': '1',
            'remarks': 'test',
            'save': 'basic'
        })
        # プロジェクトが保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/detail/' + str(project.id) in result.headers['Location'])

        project = self.project_repository.find_by_id(project_id)
        actual = project.project_name
        self.assertEqual(actual, expected)

    # プロジェクトの基本情報を保存出来ない
    def test_save_project_basic_fail(self):
        before = len(self.project_repository.find_all())
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project = self.project_repository.find_all()[0]

        project_id = project.id

        result = self.app.post('/project/detail/' + str(project_id), data={
            'project_name': project.project_name,
            'end_user': project.end_user,
            'client_company_id': project.client_company_id,
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'recorded_department_id': 'a',
            'over_time_calculation_id': project.over_time_calculation_id,
            'contract_form_id': project.contract_form_id,
            'status_id': project.status_id,
            'billing_timing': project.billing_timing,
            'remarks': project.remarks,
            'save': 'basic'
        })
        # プロジェクトが保存できないことを確認
        self.assertEqual(result.status_code, 200)

        after = len(self.project_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # プロジェクトの見積り情報を保存出来る
    def test_save_project_estimate(self):
        before = len(self.project_repository.find_all())
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project = self.project_repository.find_all()[0]

        expected = 'test_save_project_estimate'
        project_id = project.id

        result = self.app.post('/project/detail/' + str(project_id), data={
            'scope': expected,
            'contents': 'test',
            'deliverables': 'test',
            'delivery_place': 'test',
            'inspection_date': '2017/1/1',
            'responsible_person': 'test',
            'quality_control': 'test',
            'subcontractor': 'test',
            'save': 'estimate'
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/detail/' + str(project.id) in result.headers['Location'])

        project = self.project_repository.find_by_id(project_id)
        actual = project.estimation_remarks.scope
        self.assertEqual(actual, expected)

    # プロジェクトの注文請け情報を保存出来る
    def test_save_project_order(self):
        before = len(self.project_repository.find_all())
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project = self.project_repository.find_all()[0]

        expected = 'test_save_project_order'
        project_id = project.id

        result = self.app.post('/project/detail/' + str(project_id), data={
            'order_no': expected,
            'order_amount': 1,
            'contents': 'test',
            'responsible_person': 'test',
            'subcontractor': 'test',
            'scope': 'test',
            'work_place': 'test',
            'delivery_place': 'test',
            'deliverables': 'test',
            'inspection_date': '2017/1/1',
            'payment_terms': 'test',
            'billing_company_id': 1,
            'remarks': 'test',
            'save': 'order'
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/detail/' + str(project.id) in result.headers['Location'])

        project = self.project_repository.find_by_id(project_id)
        actual = project.order_remarks.order_no
        self.assertEqual(actual, expected)

    # プロジェクトをコピーできる
    def test_copy_project(self):
        # コピー用のプロジェクトを登録
        project = Project(
            project_name='test_copy_project',
            end_user='test',
            client_company_id=1,
            start_date=date.today(),
            end_date='2099/12/31',
            recorded_department_id=1,
            over_time_calculation_id=1,
            contract_form_id=1,
            estimation_no='test_copy_project',
            status_id=1,
            billing_timing='1',
            remarks='test',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')

        estimation_remarks = EstimationRemarks(
            project_id=project.id,
            scope='scope',
            contents='contents',
            deliverables='deliverables',
            delivery_place='delivery_place',
            inspection_date='2017/1/1',
            responsible_person='responsible_person',
            quality_control='quality_control',
            subcontractor='subcontractor',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')

        order_remarks = OrderRemarks(
            project_id=project.id,
            order_no='1',
            order_amount=1,
            contents='contents',
            responsible_person='responsible_person',
            subcontractor='subcontractor',
            scope='scope',
            work_place='work_place',
            delivery_place='delivery_place',
            deliverables='deliverables',
            inspection_date='2017/1/1',
            payment_terms='payment_terms',
            billing_company_id=1,
            remarks='remarks',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')

        project.estimation_remarks = estimation_remarks
        project.order_remarks = order_remarks

        db.session.add(project)
        db.session.commit()

        original_project_id = project.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        original = self.project_repository.find_by_id(original_project_id)

        result = self.app.get('/project/copy/' + str(original.id))
        # コピーできることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/detail' in result.headers['Location'])

        copy_project_id = result.headers['Location'][-1:]

        # コピーしたプロジェクトが存在することを確認
        copy = self.project_repository.find_by_id(copy_project_id)
        self.assertIsNotNone(copy.id)

    # プロジェクトを削除できる
    def test_delete_project(self):
        # 削除用のプロジェクトを登録
        project = Project(
            project_name='test_delete_project',
            end_user='test',
            client_company_id=1,
            start_date=date.today(),
            end_date='2099/12/31',
            recorded_department_id=1,
            over_time_calculation_id=1,
            contract_form_id=1,
            estimation_no='test_delete_project',
            status_id=1,
            billing_timing='1',
            remarks='test',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        delete_project_id = project.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        project = self.project_repository.find_by_id(delete_project_id)

        result = self.app.get('/project/delete/' + str(project.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project' in result.headers['Location'])

        # 削除したプロジェクトが存在しないことを確認
        project = self.project_repository.find_by_id(delete_project_id)
        self.assertIsNone(project.id)

    # 存在しないプロジェクトは削除できない
    def test_delete_project_fail(self):
        before = len(self.project_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project' in result.headers['Location'])

        after = len(self.project_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)
