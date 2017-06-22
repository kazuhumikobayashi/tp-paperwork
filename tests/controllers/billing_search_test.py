from urllib.parse import urlencode

from datetime import date, datetime

from application import db
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.project_month import ProjectMonth
from application.domain.repository.project_month_repository import ProjectMonthRepository
from tests import BaseTestCase


class BillingSearchTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(BillingSearchTests, cls).setUpClass()

    def setUp(self):
        super(BillingSearchTests, self).setUp()
        self.project_month_repository = ProjectMonthRepository()

    def tearDown(self):
        super(BillingSearchTests, self).tearDown()

    # 請求の検索画面に遷移する。
    def test_get_billing_search(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/search/billing/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_billing_search_page2(self):
        # データセットアップ
        for num in range(12):
            project_month = ProjectMonth(
                project_id=1,
                project_month=date(2017, num+1, 1),
                deposit_date=datetime.today().date(),
                billing_estimated_money=100000,
                billing_confirmation_money=100100,
                billing_transportation=100,
                remarks=None,
                client_billing_no='1000',
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
            db.session.add(project_month)
        db.session.commit()

        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/search/billing/page/2')
        self.assertEqual(result.status_code, 200)

    # 請求を検索する。
    def test_search_billing(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': 'test',
                                  'result_input_flag': '1',
                                  'billing_input_flag': '1',
                                  'deposit_input_flag': '1',
                                  'end_user_company_id': '1', 
                                  'client_company_id': '1',
                                  'recorded_department_id': '1',
                                  'deposit_date_from': '2016/1/1',         
                                  'deposit_date_to': '2017/1/1'})
        result = self.app.get('/search/billing/?' + query_string)

        self.assertEqual(result.status_code, 200)

    # 日付をブランクで請求を検索する
    def test_search_billing_blank_day(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': 'test',
                                  'result_input_flag': '1',
                                  'billing_input_flag': '1',
                                  'deposit_input_flag': '1',
                                  'end_user_company_id': '1', 
                                  'client_company_id': '1',
                                  'recorded_department_id': '1',
                                  'deposit_date_from': '',         
                                  'deposit_date_to': ''})
        result = self.app.get('/search/billing/?' + query_string)

        self.assertEqual(result.status_code, 200)

    # 入金済みフラグが更新されることを確認する
    def test_save_flag(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project_month  = self.project_month_repository.find_by_id(3)
        self.assertEqual(project_month.deposit_input_flag, InputFlag.yet)

        # 入金済みフラグをチェック有りで更新する。
        excepted = InputFlag.done.value

        headers = [('X-Requested-With', 'XMLHttpRequest')]
        result = self.app.post('/search/billing/save_flag',
                               headers=headers,
                               data={
                                    'month_id': project_month.id,
                                    'input_flag': excepted
                               })
        self.assertEqual(result.status_code, 200)

        # DBのdeposit_input_flag値が1になっていることを確認。
        project_result = self.project_month_repository.find_by_id(3)
        actual_input_flag = project_result.deposit_input_flag.value
        self.assertEqual(actual_input_flag, excepted)

    def test_save_flag_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # xhrではない場合
        result = self.app.post('/search/billing/save_flag', data={
                                    'month_id': '2',
                                    'input_flag': InputFlag.done.value
                               })
        self.assertEqual(result.status_code, 404)
