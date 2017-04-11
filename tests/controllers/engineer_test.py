from datetime import datetime, date

from nose.tools import ok_

from application import db
from application.domain.model.engineer import Engineer
from application.domain.repository.engineer_repository import EngineerRepository
from tests import BaseTestCase


class EngineerTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(EngineerTests, cls).setUpClass()

    def setUp(self):
        super(EngineerTests, self).setUp()
        self.engineer_repository = EngineerRepository()

    def tearDown(self):
        super(EngineerTests, self).tearDown()

    # 技術者の検索画面に遷移する。
    def test_get_engineer(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_engineer_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer/page/2')
        self.assertEqual(result.status_code, 200)

    # 技術者を検索する。
    def test_search_engineer(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer/?engineer_name=test&skill_id=2&company_id=2&business_category_id=2')
        self.assertEqual(result.status_code, 200)

    # 技術者登録画面に遷移する。
    def test_get_engineer_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer/create')
        self.assertEqual(result.status_code, 200)

    # 技術者登録する。
    def test_create_engineer(self):
        before = len(self.engineer_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/engineer/create', data={
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31',
            'engineer_name': 'テスト登録',
            'skill': ['1', '2'],
            'business_category': ['1', '2'],
            'company_id': '1'
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.engineer_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # 技術者詳細画面に遷移する。
    def test_get_engineer_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        engineer = self.engineer_repository.find_all()[0]

        result = self.app.get('/engineer/detail/' + str(engineer.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない技術者の場合はnot_found
    def test_get_engineer_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer/detail/0')
        self.assertEqual(result.status_code, 404)

    # 技術者を保存できる
    def test_save_engineer(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        engineer = self.engineer_repository.find_all()[0]

        expected = '単体テスト_変更'
        engineer_id = engineer.id

        result = self.app.post('/engineer/detail/' + str(engineer_id), data={
            'start_date': engineer.start_date.strftime('%Y/%m/%d'),
            'end_date': engineer.end_date.strftime('%Y/%m/%d'),
            'engineer_name': expected,
            'engineer_name_kana': engineer.engineer_name_kana,
            'company_id': engineer.company_id,
            'remarks': engineer.remarks
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/engineer/detail/' + str(engineer.id) in result.headers['Location'])

        engineer = self.engineer_repository.find_by_id(engineer_id)
        actual = engineer.engineer_name
        self.assertEqual(actual, expected)

    # エンジニアを削除できる
    def test_delete_engineer(self):
        # 削除用のエンジニアを登録
        engineer = Engineer(
            start_date=date.today(),
            end_date='2099/12/31',
            engineer_name='削除用エンジニア',
            company_id='1',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        delete_engineer_id = engineer.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        engineer = self.engineer_repository.find_by_id(delete_engineer_id)

        result = self.app.get('/engineer/delete/' + str(engineer.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/engineer' in result.headers['Location'])

        # 削除したエンジニアが存在しないことを確認
        engineer = self.engineer_repository.find_by_id(delete_engineer_id)
        self.assertIsNone(engineer.id)

    # 存在しないエンジニアは削除できない
    def test_delete_engineer_fail(self):
        before = len(self.engineer_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/engineer' in result.headers['Location'])

        after = len(self.engineer_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)
