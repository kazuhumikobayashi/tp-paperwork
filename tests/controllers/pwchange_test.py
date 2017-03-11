from tests import BaseTestCase


class PWChangeTests(BaseTestCase):

    def setUp(self):
        super(PWChangeTests, self).setUp()

    def tearDown(self):
        super(PWChangeTests, self).tearDown()

    # パスワード変更画面に遷移する。
    def test_get_root(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/pwchange')
        self.assertEqual(result.status_code, 200)

    # パスワードを変更する。
    def test_post_root(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/pwchange', data={
            'password': 'test',
            'new_password': 'test',
            'new_password_confirmation': 'test'
        })
        self.assertEqual(result.status_code, 200)

    # 現在のパスワードが違う場合はパスワードを変更に失敗する。
    def test_post_root_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/pwchange', data={
            'password': 'test1',
            'new_password': 'test',
            'new_password_confirmation': 'test'
        })
        self.assertEqual(result.status_code, 200)
