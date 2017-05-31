from urllib.parse import urlencode

from datetime import date, datetime
from nose.tools import ok_

from application import db
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

        query_string = urlencode({'project_name': 'test',
                                  'end_user_company_id': '1',
                                  'client_company_id': '1',
                                  'recorded_department_id': '1', 
                                  'start_date': '2016/1/1',                                  
                                  'end_date': '2017/1/1'})
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

    # 次の期の基本情報を保存できる
    def test_create_project_second_basic(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })

        result = self.app.post('/project/create', data={
            'project_name': 'test_create_project_basic',
            'end_user_company_id': '1',
            'client_company_id': '1',
            'start_date': str(int(datetime.today().strftime('%Y')) + 1) + '/4/1',
            'end_date': '2099/12/31',
            'recorded_department_id': '1',
            'over_time_calculation_id': '1',
            'contract_form_id': '1',
            'status_id': '1',
            'billing_timing': '契約期間末1回',
            'remarks': 'test',
            'save': 'basic'
        })
        # プロジェクトが保存できることを確認
        self.assertEqual(result.status_code, 302)

    # プロジェクトをコピーできる
    def test_copy_project(self):
        # コピー用のプロジェクトを登録
        project = Project(
            project_name='test_copy_project',
            status='01:契約開始',
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='test_copy_project',
            end_user_company_id=1,
            client_company_id=5,
            start_date=date.today(),
            end_date='2099/12/31',
            contract_form='請負契約（一括契約）',
            billing_timing='契約期間末1回',
            estimated_total_amount=1000000,
            deposit_date='2099/12/31',
            scope='test',
            contents=None,
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
        # ok_('/project/detail' in result.headers['Location'])

        # copy_project_id = result.headers['Location'][-1:]

        # コピーしたプロジェクトが存在することを確認
        # copy = self.project_repository.find_by_id(copy_project_id)
        # self.assertIsNotNone(copy.id)

    # プロジェクトを削除できる
    def test_delete_project(self):
        # 削除用のプロジェクトを登録
        project = Project(
            project_name='test_delete_project',
            status='01:契約開始',
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='test_delete_project',
            end_user_company_id=1,
            client_company_id=5,
            start_date=date.today(),
            end_date='2099/12/31',
            contract_form='請負契約（一括契約）',
            billing_timing='契約期間末1回',
            estimated_total_amount=1000000,
            deposit_date='2099/12/31',
            scope='test',
            contents=None,
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
