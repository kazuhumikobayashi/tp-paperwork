from nose.tools import ok_

from tests import BaseTestCase


class LoginTests(BaseTestCase):

    def setUp(self):
        super(LoginTests, self).setUp()

    def tearDown(self):
        super(LoginTests, self).tearDown()

    # ログイン画面に遷移する。
    def test_get_login(self):
        result = self.app.get('/login')

        self.assertEqual(result.status_code, 200)

    # ログインできることを確認
    def test_login(self):
        result = self.app.post('/login', data={
            'shain_number': 'test',
            'password': 'test'
        })
        self.assertEqual(result.status_code, 302)
        ok_('/' in result.headers['Location'])

    # 社員番号が存在しない場合はログインできない
    def test_login_fail(self):
        result = self.app.post('/login', data={
            'shain_number': 'not_exist_user',
            'password': 'test'
        })
        self.assertEqual(result.status_code, 200)

    # ログアウトできることを確認
    def test_logout(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test',
            'password': 'test'
        })
        result = self.app.get('/logout')
        self.assertEqual(result.status_code, 302)
        ok_('/login' in result.headers['Location'])
