from nose.tools import ok_

from application.domain.repository.project_month_repository import ProjectMonthRepository
from tests import BaseTestCase


class ProjectMonthTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectMonthTests, cls).setUpClass()

    def setUp(self):
        super(ProjectMonthTests, self).setUp()
        self.project_month_repository = ProjectMonthRepository()

    def tearDown(self):
        super(ProjectMonthTests, self).tearDown()

    # 請求タブに遷移する。
    def test_get_project_billing(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_billing = self.project_month_repository.find_all()[0]

        result = self.app.get('/project_billing/' + str(project_billing.project.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないプロジェクトの場合はnot_found
    def test_get_project_billing_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project_billing/0')
        self.assertEqual(result.status_code, 404)

    # 請求詳細画面に遷移する。
    def test_get_project_billing_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_billing = self.project_month_repository.find_all()[0]

        result = self.app.get('/project_billing/detail/' + str(project_billing.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないプロジェクト年月の場合はnot_found
    def test_get_project_billing_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project_billing/detail/0')
        self.assertEqual(result.status_code, 404)

    # 請求詳細画面を保存できる
    def test_save_project_billing(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_billing = self.project_month_repository.find_all()[0]

        expected = '単体テスト_変更'
        project_billing_id = project_billing.id

        result = self.app.post('/project_billing/detail/' + str(project_billing_id), data={
            'client_billing_no': expected,
            'billing_confirmation_money': project_billing.billing_confirmation_money,
            'billing_transportation': project_billing.billing_transportation,
            'deposit_date': project_billing.deposit_date.strftime('%Y/%m/%d'),
            'remarks': project_billing.remarks
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project_billing/detail/' + str(project_billing.id) in result.headers['Location'])

        project_billing = self.project_month_repository.find_by_id(project_billing_id)
        actual = project_billing.client_billing_no
        self.assertEqual(actual, expected)
