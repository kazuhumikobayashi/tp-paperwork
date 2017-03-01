from application.domain.repository.user_repository import UserRepository
from tests import BaseTestCase


class AssignedMemberTests(BaseTestCase):

    def setUp(self):
        super(AssignedMemberTests, self).setUp()
        self.user_repository = UserRepository()

    def tearDown(self):
        super(AssignedMemberTests, self).tearDown()

    def test_test(self):
        user = self.user_repository.find_all()
        self.assertEqual(2, len(user))
