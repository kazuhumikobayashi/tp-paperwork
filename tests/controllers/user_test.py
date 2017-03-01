from datetime import datetime

from nose.tools import ok_

from application import bcrypt, db
from application.domain.model.user import User
from application.domain.repository.user_repository import UserRepository
from tests import BaseTestCase


class UserTests(BaseTestCase):

    def setUp(self):
        super(UserTests, self).setUp()
        self.user_repository = UserRepository()

    def tearDown(self):
        super(UserTests, self).tearDown()

    # ユーザー検索画面に遷移する。
    def test_get_user(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/user/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_user_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/user/page/2')
        self.assertEqual(result.status_code, 200)

    # ユーザー登録画面に遷移する。
    def test_get_user_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/user/create')
        self.assertEqual(result.status_code, 200)

    # ユーザー詳細画面に遷移する。
    def test_get_user_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        user = self.user_repository.find_by_shain_number(shain_number)

        result = self.app.get('/user/detail/' + str(user.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないユーザーの場合はnot_found
    def test_get_user_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/user/detail/0')
        self.assertEqual(result.status_code, 404)

    # ユーザー情報を保存できる
    def test_save_user(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        user = self.user_repository.find_by_shain_number(shain_number)

        expected = '単体テスト_変更'

        result = self.app.post('/user/detail/' + str(user.id), data={
            'shain_number': user.shain_number,
            'user_name': expected,
            'mail': user.mail
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/user/detail/' + str(user.id) in result.headers['Location'])

        user = self.user_repository.find_by_shain_number(shain_number)
        actual = user.user_name
        self.assertEqual(actual, expected)

    # ユーザー情報を削除できる
    def test_delete_user(self):
        # 削除用のユーザーを登録
        user = User(
                 shain_number='delete_user',
                 user_name='削除用ユーザー',
                 mail='test@delete.com',
                 password=bcrypt.generate_password_hash('test'),
                 created_at=datetime.today(),
                 created_user='test',
                 updated_at=datetime.today(),
                 updated_user='test')
        db.session.add(user)
        db.session.commit()

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        user = self.user_repository.find_by_shain_number('delete_user')

        result = self.app.get('/user/delete/' + str(user.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/user' in result.headers['Location'])

        # 削除したユーザーが存在しないことを確認
        user = self.user_repository.find_by_shain_number('delete_user')
        self.assertIsNone(user)

    # 存在しないユーザーは削除できない
    def test_delete_user_fail(self):
        before = len(self.user_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/user/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/user' in result.headers['Location'])

        after = len(self.user_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)
