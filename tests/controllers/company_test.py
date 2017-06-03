from datetime import datetime

from nose.tools import ok_

from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.tax import Tax
from tests import BaseTestCase

from application import db
from application.domain.model.company import Company
from application.domain.repository.company_repository import CompanyRepository


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

        result = self.app.get('/company/?company_name=test&client_flag_id=2&bank_id=2')
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
            'company_name': company.company_name,
            'company_name_kana': expected,
            'contract_date': datetime.today().strftime('%Y/%m/%d'),
            'client_flag': [ClientFlag.bp.value, ClientFlag.client.value],
            'postal_code': company.postal_code,
            'address': company.address,
            'phone': company.phone,
            'fax': company.fax,
            'client_code': company.client_code,
            'bp_code': company.bp_code,
            'payment_site': company.payment_site,
            'receipt_site': company.receipt_site,
            'payment_tax': company.payment_tax,
            'receipt_tax': company.receipt_tax,
            'bank_id': '1',
            'bank_holiday_flag': company.bank_holiday_flag,
            'remarks': company.remarks,
            'print_name': company.print_name
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/company/detail/' + str(company.id) in result.headers['Location'])

        company = self.company_repository.find_by_id(company_id)
        actual = company.company_name_kana
        self.assertEqual(actual, expected)

    # 会社情報を削除できる
    def test_delete_company(self):
        # 削除用のユーザーを登録
        company = Company(
            company_name='削除用会社',
            contract_date=datetime.today().strftime('%Y/%m/%d'),
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

        # 削除した会社が存在しないことを確認
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

    # 会社が顧客の場合、「顧客コード」「入金サイト」「入金消費税区分」「振込先銀行」「振込先銀行休日時フラグ」が必須
    def test_not_null_by_client(self):
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        company_id = 2
        company_before = self.company_repository.find_by_id(company_id)
        
        # 顧客の場合に、nullで更新。
        result = self.app.post('/company/detail/' + str(company_id), data={
            'company_name': 'test_not_null_by_client',
            'client_flag': [ClientFlag.client.value],
            'client_code': '',
            'payment_site': '',
            'payment_tax': '',
            'bank_id': '',
            'bank_holiday_flag': ''
        })
        self.assertEqual(result.status_code, 200)
        
        # nullで更新出来なかったことを確認する。
        company_after = self.company_repository.find_by_id(company_id)
        self.assertEqual(company_before.client_code, company_after.client_code)
        self.assertEqual(company_before.payment_site, company_after.payment_site)
        self.assertEqual(company_before.payment_tax, company_after.payment_tax)
        self.assertEqual(company_before.bank_id, company_after.bank_id)
        self.assertEqual(company_before.bank_holiday_flag, company_after.bank_holiday_flag)

    # 会社がBP所属の場合、「協力会社コード」「支払サイト」「支払消費税区分」が必須
    def test_not_null_by_BP(self):
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        company_id = 3
        company_before = self.company_repository.find_by_id(company_id)
        
        # 「協力会社コード」「支払サイト」「支払消費税区分」に値を入れておく
        company_before.bp_code = '9999'
        company_before.receipt_site = Site.twenty_five
        company_before.receipt_tax = Tax.eight
        db.session.commit()

        # BPの場合に、nullで更新。
        self.app.post('/company/detail/' + str(company_id), data={
            'company_name': 'test_not_null_by_BP',
            'client_flag': [ClientFlag.bp.value],
            'bp_code': '',
            'receipt_site': '',
            'receipt_tax': ''
        })

        # nullで更新出来なかったことを確認する。
        company_after = self.company_repository.find_by_id(company_id)
        self.assertEqual(company_before.bp_code, company_after.bp_code)
        self.assertEqual(company_before.receipt_site, company_after.receipt_site)
        self.assertEqual(company_before.receipt_tax, company_after.receipt_tax)

    # 会社情報を新規登録できる
    def test_create_company(self):
        before = len(self.company_repository.find_all())
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/company/create', data={
            'company_name': 'test99',
            'company_name_kana': 'テスト99',
            'contract_date': datetime.today().strftime('%Y/%m/%d'),
            'client_flag': [ClientFlag.bp.value],
            'postal_code': '111-1111',
            'address': '住所２',
            'phone': '111-1111',
            'fax': '111-1111',
            'client_code': '0001',
            'bp_code': '9999',
            'payment_site': 30,
            'receipt_site': 25,
            'payment_tax': 0,
            'receipt_tax': 10,
            'bank_id': '1',
            'bank_holiday_flag': 1,
            'remarks': '備考',
            'print_name': '印刷用宛名',
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.company_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)
    
    # client_flag「自社」は一社のみ
    def test_only_one_our_company(self):
        # 「自社」の会社を抽出
        before = len(self.company_repository.find_by_client_flag([ClientFlag.our_company.value]))
        # 「自社」の会社が1件あることを確認
        self.assertEqual(before, 1)

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/company/create', data={
            'company_name': 'test_only_one_our_company',
            'client_flag': [ClientFlag.our_company.value],
            'client_code': '',
            'payment_tax': '',
            'receipt_tax': '',
            'bank_id': '',
            'bank_holiday_flag': ''
        })
        self.assertEqual(result.status_code, 200)
        
        # 件数が変わっていないことを確認する。
        after = len(self.company_repository.find_by_client_flag([ClientFlag.our_company.value]))
        self.assertEqual(before, after)
