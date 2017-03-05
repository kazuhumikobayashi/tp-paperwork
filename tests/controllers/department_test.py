from datetime import datetime, date

from nose.tools import ok_

from application import db
from application.domain.model.department import Department
from application.domain.repository.department_repository import DepartmentRepository
from tests import BaseTestCase


class DepartmentTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(DepartmentTests, cls).setUpClass()
        cls().create_departments()

    def setUp(self):
        super(DepartmentTests, self).setUp()
        self.department_repository = DepartmentRepository()

    def tearDown(self):
        super(DepartmentTests, self).tearDown()

    # 部署の検索画面に遷移する。
    def test_get_department(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/department/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_department_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/department/page/2')
        self.assertEqual(result.status_code, 200)

    # 部署を検索する。
    def test_search_department(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/department/?department_code=test&department_name=test')
        self.assertEqual(result.status_code, 200)

    # 部署登録画面に遷移する。
    def test_get_department_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/department/create')
        self.assertEqual(result.status_code, 200)

    # 部署登録する。
    def test_create_department(self):
        before = len(self.department_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/department/create', data={
            'department_code': '0001',
            'department_name': 'テスト登録'
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.department_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # 部署詳細画面に遷移する。
    def test_get_department_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        department = self.department_repository.find_all()[0]

        result = self.app.get('/department/detail/' + str(department.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない部署の場合はnot_found
    def test_get_department_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/department/detail/0')
        self.assertEqual(result.status_code, 404)

    # 部署を保存できる
    def test_save_department(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        department = self.department_repository.find_all()[0]

        expected = '単体テスト_変更'
        department_id = department.id

        result = self.app.post('/department/detail/' + str(department_id), data={
            'department_name': expected,
            'department_code': department.department_code
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/department/detail/' + str(department.id) in result.headers['Location'])

        department = self.department_repository.find_by_id(department_id)
        actual = department.department_name
        self.assertEqual(actual, expected)

    # 部署を削除できる
    def test_delete_department(self):
        # 削除用の部署を登録
        department = Department(
            department_code='delete_department',
            department_name='削除用部署',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(department)
        db.session.commit()

        delete_department_id = department.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        department = self.department_repository.find_by_id(delete_department_id)

        result = self.app.get('/department/delete/' + str(department.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/department' in result.headers['Location'])

        # 削除したエンジニアが存在しないことを確認
        department = self.department_repository.find_by_id(delete_department_id)
        self.assertIsNone(department.id)

    # 存在しない部署は削除できない
    def test_delete_department_fail(self):
        before = len(self.department_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/department/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/department' in result.headers['Location'])

        after = len(self.department_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    def create_departments(self):
        for num in range(12):
            department = Department(
                department_code='test' + str(num),
                department_name='単体テスト' + str(num),
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
            db.session.add(department)
        db.session.commit()
