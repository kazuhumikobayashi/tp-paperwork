from application.domain.repository.status_repository import StatusRepository
from tests import BaseTestCase


class StatusRepositoryTests(BaseTestCase):

    def setUp(self):
        super(StatusRepositoryTests, self).setUp()
        self.status_repository = StatusRepository()

    def tearDown(self):
        super(StatusRepositoryTests, self).tearDown()

    def test_find_by_name(self):
        expected = '見積り中'
        status = self.status_repository.find_by_name(expected)
        actual = status.status_name
        self.assertEqual(actual, expected)

    def test_create(self):
        status = self.status_repository.create()
        self.assertIsNone(status.id)
