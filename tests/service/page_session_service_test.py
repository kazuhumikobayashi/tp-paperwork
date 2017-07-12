import unittest

from flask import session

from application import app
from application.service.page_session_service import PageSessionService


class PageSessionServiceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(PageSessionServiceTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(PageSessionServiceTests, cls).tearDownClass()

    def setUp(self):
        super(PageSessionServiceTests, self).setUp()

    def tearDown(self):
        super(PageSessionServiceTests, self).tearDown()

    def test_get_dict(self):
        with app.test_request_context():
            # testページへ遷移
            excepted = 'test'
            page = PageSessionService(excepted)

            # saveしていない場合は、sessionにNoneが返却される
            self.assertIsNone(session.get('pre_page'))

            # saveすると保存したページを取得できる。
            page.save()
            self.assertEqual(session.get('pre_page'), excepted)

            # ページをNoneでインスタンスを生成するとNoneが返却される
            page = PageSessionService(None)
            page.save()
            self.assertIsNone(session.get('pre_page'))
