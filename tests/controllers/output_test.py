from application.domain.model.immutables.output_type import OutputType
from tests import BaseTestCase


class OutputTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(OutputTests, cls).setUpClass()

    def setUp(self):
        super(OutputTests, self).setUp()

    def tearDown(self):
        super(OutputTests, self).tearDown()

    # 帳票出力画面に遷移する。
    def test_get_output(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/output/')
        self.assertEqual(result.status_code, 200)
