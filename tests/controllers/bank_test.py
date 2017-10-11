from datetime import datetime

from nose.tools import ok_

from application import db
from application.domain.model.bank import Bank
from application.domain.repository.bank_repository import BankRepository
from tests import BaseTestCase


class BankTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(BankTests, cls).setUpClass()

    def setUp(self):
        super(BankTests, self).setUp()
        self.bank_repository = BankRepository()

    def tearDown(self):
        super(BankTests, self).tearDown()

    # 銀行の検索画面に遷移する。
    def test_get_bank(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/bank/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_bank_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        print(self.bank_repository.find_all())

        result = self.app.get('/bank/page/2?bank_name=&text_for_document=')
        self.assertEqual(result.status_code, 200)

    # 銀行を検索する。
    def test_search_bank(self):

        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/bank/?bank_name=test&text_for_document=単体テスト')
        self.assertEqual(result.status_code, 200)

    # 銀行をブランクで検索する。
    def test_search_bank_year_blank(self):

        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/bank/?year=')
        self.assertEqual(result.status_code, 200)

    # 銀行登録画面に遷移する。
    def test_get_bank_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/bank/create')
        self.assertEqual(result.status_code, 200)

    # 銀行登録する。
    def test_create_bank(self):
        before = len(self.bank_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/bank/create', data={
            'bank_name': 'テスト登録',
            'text_for_document': 'テスト_書類提出用文言名称'
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.bank_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # 銀行登録に失敗する。
    def test_create_skill_fail(self):
        before = len(self.bank_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 名称をブランクで登録できない
        result = self.app.post('/bank/create', data={
            'bank_name': '',
            'text_for_document': ''
        })
        self.assertEqual(result.status_code, 200)

        after = len(self.bank_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 銀行詳細画面に遷移する。
    def test_get_bank_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        bank = self.bank_repository.find_all()[0]

        result = self.app.get('/bank/detail/' + str(bank.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない銀行の場合はnot_found
    def test_get_bank_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/bank/detail/0')
        self.assertEqual(result.status_code, 404)

    # 銀行を保存できる
    def test_save_bank(self):
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        bank = self.bank_repository.find_all()[0]

        expected = '単体テスト_変更'
        bank_id = bank.id

        result = self.app.post('/bank/detail/' + str(bank_id), data={
            'bank_name': expected,
            'text_for_document': bank.text_for_document
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/bank/detail/' + str(bank.id) in result.headers['Location'])

        bank = self.bank_repository.find_by_id(bank_id)
        actual = bank.bank_name
        self.assertEqual(actual, expected)

    # 銀行を削除できる
    def test_delete_bank(self):
        # 削除用の銀行を登録
        bank = Bank(
            bank_name='削除用銀行',
            text_for_document='単体テスト',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(bank)
        db.session.commit()

        delete_bank_id = bank.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        bank = self.bank_repository.find_by_id(delete_bank_id)

        result = self.app.get('/bank/delete/' + str(bank.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/bank' in result.headers['Location'])

        # 削除した銀行が存在しないことを確認
        bank = self.bank_repository.find_by_id(delete_bank_id)
        self.assertIsNone(bank.id)

    # 存在しない銀行は削除できない
    def test_delete_bank_fail(self):
        before = len(self.bank_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/bank/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/bank' in result.headers['Location'])

        after = len(self.bank_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)
