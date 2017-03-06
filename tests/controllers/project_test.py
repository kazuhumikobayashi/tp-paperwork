from urllib.parse import urlencode

from nose.tools import ok_

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
                                               'client_company_id': '1'})
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

    # # プロジェクトを登録する。
    # def test_create_project(self):
    #     before = len(self.project_repository.find_all())
    #     # ログインする
    #     self.app.post('/login', data={
    #         'shain_number': 'test1',
    #         'password': 'test'
    #     })
    #
    #     result = self.app.post('/project/create', data={
    #         'amount': '9999',
    #         'formula': '1',
    #     })
    #     self.assertEqual(result.status_code, 302)
    #
    #     after = len(self.project_repository.find_all())
    #     # 1件追加されていることを確認
    #     self.assertEqual(before + 1, after)

    # # プロジェクト登録に失敗する。
    # def test_create_project_fail(self):
    #     before = len(self.project_repository.find_all())
    #     # ログインする
    #     self.app.post('/login', data={
    #         'shain_number': 'test1',
    #         'password': 'test'
    #     })
    #
    #     # 同じ見積りNoのプロジェクトは登録できない
    #     result = self.app.post('/project/create', data={
    #         'amount': '0',
    #         'formula': '1',
    #     })
    #     self.assertEqual(result.status_code, 200)
    #
    #     after = len(self.project_repository.find_all())
    #     # 前後で件数が変わっていないことを確認
    #     self.assertEqual(before, after)

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

    # # プロジェクトを保存できる
    # def test_save_project(self):
    #     shain_number = 'test1'
    #     self.app.post('/login', data={
    #         'shain_number': shain_number,
    #         'password': 'test'
    #     })
    #     project = self.project_repository.find_all()[0]
    #
    #     expected = '10000円未満切り捨て'
    #     project_id = project.id
    #
    #     result = self.app.post('/project/detail/' + str(project_id), data={
    #         'amount': '10000',
    #         'formula': '1',
    #     })
    #     # プロジェクトできることを確認
    #     self.assertEqual(result.status_code, 302)
    #     ok_('/project/detail/' + str(project.id) in result.headers['Location'])
    #
    #     project = self.project_repository.find_by_id(project_id)
    #     actual = project.project_name
    #     self.assertEqual(actual, expected)

    # # プロジェクトを削除できる
    # def test_delete_project(self):
    #     # 削除用のプロジェクトを登録
    #     project = Project(
    #         project_name='100000円未満切り捨て',
    #         amount=100000,
    #         formula=1,
    #         created_at=datetime.today(),
    #         created_user='test',
    #         updated_at=datetime.today(),
    #         updated_user='test')
    #     db.session.add(project)
    #     db.session.commit()
    #
    #     delete_project_id = project.id
    #
    #     # ログイン
    #     self.app.post('/login', data={
    #         'shain_number': 'test1',
    #         'password': 'test'
    #     })
    #     project = self.project_repository.find_by_id(delete_project_id)
    #
    #     result = self.app.get('/project/delete/' + str(project.id))
    #     # 削除できることを確認
    #     self.assertEqual(result.status_code, 302)
    #     ok_('/project' in result.headers['Location'])
    #
    #     # 削除したエンジニアが存在しないことを確認
    #     project = self.project_repository.find_by_id(delete_project_id)
    #     self.assertIsNone(project.id)

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
