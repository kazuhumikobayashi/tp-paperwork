import unittest

from werkzeug.datastructures import ImmutableMultiDict

from application.domain.model.form.search import Search


class SearchTests(unittest.TestCase):
    def setUp(self):
        super(SearchTests, self).setUp()

    def tearDown(self):
        super(SearchTests, self).tearDown()

    def test___repr__(self):
        search = Search(page='page', request_args=ImmutableMultiDict({'test': 'test'}))

        expected = "<Search:" + \
                   "'request_args='{}".format(search.request_args) + \
                   "', page='{}".format(search.page) + \
                   "'>"

        actual = str(search)
        self.assertEqual(actual, expected)
