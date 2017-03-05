from nose.tools import ok_

from tests import BaseTestCase


class RootTests(BaseTestCase):

    def setUp(self):
        super(RootTests, self).setUp()

    def tearDown(self):
        super(RootTests, self).tearDown()

    # ルート画面に遷移する。
    def test_get_root(self):
        # ログインする
        result = self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        self.assertEqual(result.status_code, 302)
        ok_('/' in result.headers['Location'])

        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    # ログインしていない場合はログイン画面に遷移する。
    def test_get_root_fail(self):
        # ログアウトする
        self.app.get('/logout')

        result = self.app.get('/')
        self.assertEqual(result.status_code, 302)
        ok_('/login' in result.headers['Location'])

    # ログインしていない場合でもstaticについてはアクセス可能
    def test_get_static_access(self):
        # ログアウトする
        result = self.app.get('/static/css/application.css')

        self.assertEqual(result.status_code, 200)
