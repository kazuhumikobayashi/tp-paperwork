import unittest

from werkzeug.datastructures import ImmutableMultiDict

from application import app
from application.service.search_session_service import SearchSessionService


class SearchSessionServiceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(SearchSessionServiceTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(SearchSessionServiceTests, cls).tearDownClass()

    def setUp(self):
        super(SearchSessionServiceTests, self).setUp()

    def tearDown(self):
        super(SearchSessionServiceTests, self).tearDown()

    def test_get_dict(self):
        with app.test_request_context():
            # testページで検索条件
            excepted = ImmutableMultiDict({'test': 'test'})
            search = SearchSessionService('test', excepted)

            # saveしていない場合は、get_dictでNoneが返却される
            self.assertIsNone(search.get_dict())

            # saveすると、get_dictで保存した検索条件を取得できる。
            search.save()
            self.assertEqual(search.get_dict(), excepted)

            # pageを変更すると、get_dictでNoneが返却される
            search = SearchSessionService('test2', excepted)
            search.save()
            self.assertEqual(search.get_dict(), excepted)
