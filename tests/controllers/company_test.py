from datetime import datetime, date

from nose.tools import ok_

from application import db
from application.domain.model.company import Company
from application.domain.repository.company_repository import CompanyRepository
from tests import BaseTestCase


class CompanyTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(CompanyTests, cls).setUpClass()

    def setUp(self):
        super(CompanyTests, self).setUp()
        self.company_repository = CompanyRepository()

    def tearDown(self):
        super(CompanyTests, self).tearDown()

    # 会社情報の検索画面に遷移する。
    def test_get_company(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/company/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_company_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/company/page/2')
        self.assertEqual(result.status_code, 200)

    # 会社情報を検索する。
    def test_search_company(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/company/?company_name=test&company_code=test')
        self.assertEqual(result.status_code, 200)

    # 会社登録画面に遷移する。
    def test_get_company_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/company/create')
        self.assertEqual(result.status_code, 200)

    # 会社詳細画面に遷移する。
    def test_get_company_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        company = self.company_repository.find_all()[0]

        result = self.app.get('/company/detail/' + str(company.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない会社の場合はnot_found
    def test_get_company_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/company/detail/0')
        self.assertEqual(result.status_code, 404)

    # 会社情報を保存できる
    def test_save_company(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        company = self.company_repository.find_all()[0]

        expected = '単体テスト_変更'
        company_id = company.id

        result = self.app.post('/company/detail/' + str(company_id), data={
            'company_code': company.company_code,
            'company_name': expected,
            'company_name_kana': company.company_name_kana,
            'trade_name': company.trade_name,
            'trade_name_position': '1',
            'client_flg': company.client_flg,
            'consignment_flg': company.consignment_flg,
            'start_date': company.start_date.strftime('%Y/%m/%d'),
            'end_date': company.end_date.strftime('%Y/%m/%d'),
            'postal_code': company.postal_code,
            'address1': company.address1,
            'address2': company.address2,
            'phone': company.phone,
            'fax': company.fax,
            'payment_site': company.payment_site,
            'receipt_site': company.receipt_site,
            'tax': company.tax,
            'remarks': company.remarks
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/company/detail/' + str(company.id) in result.headers['Location'])

        company = self.company_repository.find_by_id(company_id)
        actual = company.company_name
        self.assertEqual(actual, expected)

    # 会社情報を削除できる
    def test_delete_company(self):
        # 削除用のユーザーを登録
        company = Company(
            company_code='delete_company',
            company_name='削除用会社',
            client_flg='1',
            consignment_flg='1',
            start_date=date.today(),
            end_date='2099/12/31',
            tax='1',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        delete_company_id = company.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        company = self.company_repository.find_by_id(delete_company_id)

        result = self.app.get('/company/delete/' + str(company.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/company' in result.headers['Location'])

        # 削除したユーザーが存在しないことを確認
        company = self.company_repository.find_by_id(delete_company_id)
        self.assertIsNone(company.id)

    # 存在しない会社は削除できない
    def test_delete_company_fail(self):
        before = len(self.company_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/company/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/company' in result.headers['Location'])

        after = len(self.company_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)
