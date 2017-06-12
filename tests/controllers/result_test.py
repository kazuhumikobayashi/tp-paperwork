from decimal import Decimal
from nose.tools import ok_

from tests import BaseTestCase

from application.domain.repository.project_result_repository import ProjectResultRepository


class ResultTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ResultTests, cls).setUpClass()

    def setUp(self):
        super(ResultTests, self).setUp()
        self.project_result_repository = ProjectResultRepository()

    def tearDown(self):
        super(ResultTests, self).tearDown()

    # 実績登録画面に遷移する。
    def test_get_result(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project_result = self.project_result_repository.find_all()[0]

        result = self.app.get('/result/' + str(project_result.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない実績の場合はnot_found
    def test_get_result_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/result/0')
        self.assertEqual(result.status_code, 404)

    # 実績を保存できる
    def test_save_result(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_result = self.project_result_repository.find_all()[0]

        expected = Decimal(300)
        project_result_id = project_result.id

        result = self.app.post('/result/' + str(project_result_id), data={
            'work_time': expected
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/result/' + str(project_result.id) in result.headers['Location'])

        project_result = self.project_result_repository.find_by_id(project_result_id)
        actual = project_result.work_time
        self.assertEqual(actual, expected)

    # engineer_historyがない技術者を登録。
    def test_save_proper_engineer(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_result = self.project_result_repository.find_all()[2]

        # engineer_historyがないことを確認。
        self.assertEqual(project_result.project_detail.engineer.engineer_histories, [])

        expected = Decimal(300)
        project_result_id = project_result.id

        result = self.app.post('/result/' + str(project_result_id), data={
            'work_time': expected
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/result/' + str(project_result.id) in result.headers['Location'])

        project_result = self.project_result_repository.find_by_id(project_result_id)
        actual = project_result.work_time
        self.assertEqual(actual, expected)
