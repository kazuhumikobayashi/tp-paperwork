from datetime import datetime, date

from nose.tools import ok_

from application import db
from application.domain.model.tax import Tax
from application.domain.repository.tax_repository import TaxRepository
from tests import BaseTestCase


class TaxTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(TaxTests, cls).setUpClass()

    def setUp(self):
        super(TaxTests, self).setUp()
        self.tax_repository = TaxRepository()

    def tearDown(self):
        super(TaxTests, self).tearDown()

    # 消費税の検索画面に遷移する。
    def test_get_tax(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/tax/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_tax_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/tax/page/2')
        self.assertEqual(result.status_code, 200)

    # 消費税を検索する。
    def test_search_tax(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/tax/?tax_rate=1')
        self.assertEqual(result.status_code, 200)

    # 消費税登録画面に遷移する。
    def test_get_tax_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/tax/create')
        self.assertEqual(result.status_code, 200)

    # 消費税を登録する。
    def test_create_tax(self):
        before = len(self.tax_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/tax/create', data={
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31',
            'tax_rate': '1',
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.tax_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # 消費税登録に失敗する。
    def test_create_tax_fail(self):
        before = len(self.tax_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 数値以外の消費税は登録できない
        result = self.app.post('/tax/create', data={
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/311',
            'tax_rate': 'a',
        })
        self.assertEqual(result.status_code, 200)

        after = len(self.tax_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 消費税詳細画面に遷移する。
    def test_get_tax_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        tax = self.tax_repository.find_all()[0]

        result = self.app.get('/tax/detail/' + str(tax.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない消費税の場合はnot_found
    def test_get_tax_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/tax/detail/0')
        self.assertEqual(result.status_code, 404)

    # 消費税を保存できる
    def test_save_tax(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        tax = self.tax_repository.find_all()[0]

        expected = 100.00
        tax_id = tax.id

        result = self.app.post('/tax/detail/' + str(tax_id), data={
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31',
            'tax_rate': '100.00',
        })
        # 消費税を保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/tax/detail/' + str(tax.id) in result.headers['Location'])

        tax = self.tax_repository.find_by_id(tax_id)
        actual = tax.tax_rate
        self.assertEqual(actual, expected)

    # 消費税を削除できる
    def test_delete_tax(self):
        # 削除用の消費税を登録
        tax = Tax(
            start_date=date.today(),
            end_date='2099/12/31',
            tax_rate=20,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(tax)
        db.session.commit()

        delete_tax_id = tax.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        tax = self.tax_repository.find_by_id(delete_tax_id)

        result = self.app.get('/tax/delete/' + str(tax.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/tax' in result.headers['Location'])

        # 削除した消費税が存在しないことを確認
        tax = self.tax_repository.find_by_id(delete_tax_id)
        self.assertIsNone(tax.id)

    # 存在しない消費税は削除できない
    def test_delete_tax_fail(self):
        before = len(self.tax_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/tax/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/tax' in result.headers['Location'])

        after = len(self.tax_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)
