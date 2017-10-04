from urllib.parse import urlencode

from datetime import date, datetime

from application import db
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.project_result import ProjectResult
from application.domain.repository.project_result_repository import ProjectResultRepository
from tests import BaseTestCase


class SearchPaymentTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(SearchPaymentTests, cls).setUpClass()

    def setUp(self):
        super(SearchPaymentTests, self).setUp()
        self.project_result_repository = ProjectResultRepository()

    def tearDown(self):
        super(SearchPaymentTests, self).tearDown()

    # 支払の検索画面に遷移する。
    def test_get_payment(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/search/payment/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_payment_page2(self):
        # データセットアップ
        for num in range(12):
            project_result = ProjectResult(
                project_detail_id=2,
                result_month=date(2016, num+1, 1),
                work_time=160.5,
                billing_transportation=0,
                billing_confirmation_number='1人月',
                billing_confirmation_money=1000000,
                payment_transportation=1000,
                payment_confirmation_money=701000,
                remarks='テスト',
                payment_expected_date=datetime.today().date(),
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
            db.session.add(project_result)
        db.session.commit()

        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/search/payment/page/2')
        self.assertEqual(result.status_code, 200)

    # 支払を検索する。
    def test_search_payment(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': 'test',
                                  'estimation_no': 'test',
                                  'input_flag': '0',
                                  'end_user_company_id': '1',
                                  'client_company_id': '1',
                                  'recorded_department_id': '1', 
                                  'engineer_name': 'test',
                                  'payment_expected_date_from': '2016/1/1',                                  
                                  'payment_expected_date_to': '2017/1/1'})
        result = self.app.get('/search/payment/?' + query_string)

        self.assertEqual(result.status_code, 200)

    # 日付をブランクで支払を検索する。
    def test_search_payment_blank_day(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': 'test',
                                  'estimation_no': 'test',
                                  'input_flag': '0',
                                  'end_user_company_id': '1',
                                  'client_company_id': '1',
                                  'recorded_department_id': '1', 
                                  'engineer_name': 'test',
                                  'payment_expected_date_from': '',                                  
                                  'payment_expected_date_to': ''})
        result = self.app.get('/search/payment/?' + query_string)

        self.assertEqual(result.status_code, 200)

    # 支払済みフラグが更新されることを確認する
    def test_save_flag(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project_result = self.project_result_repository.find_by_id(3)
        self.assertEqual(project_result.payment_flag, InputFlag.yet)

        # 実支払済みフラグをチェック有りで更新する。
        excepted = InputFlag.done.value

        headers = [('X-Requested-With', 'XMLHttpRequest')]
        result = self.app.post('/search/payment/save_flag',
                               headers=headers,
                               data={
                                    'payment_id': project_result.id,
                                    'input_flag': excepted
                               })
        self.assertEqual(result.status_code, 200)

        # DBのpayment_flag値が1になっていることを確認。
        project_result = self.project_result_repository.find_by_id(3)
        actual_input_flag = project_result.payment_flag.value
        self.assertEqual(actual_input_flag, excepted)

    def test_save_flag_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # xhrではない場合
        result = self.app.post('/search/payment/save_flag', data={
                                    'payment_id': '2',
                                    'input_flag': InputFlag.done.value
                               })
        self.assertEqual(result.status_code, 404)
