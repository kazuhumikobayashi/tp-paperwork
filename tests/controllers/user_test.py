from application.domain.repository.user_repository import UserRepository
from tests import BaseTestCase


class UserTests(BaseTestCase):

    def setUp(self):
        super(UserTests, self).setUp()
        self.repository = UserRepository()

    def tearDown(self):
        super(UserTests, self).tearDown()
