from application.domain.repository.client_flag_repository import ClientFlagRepository
from tests import BaseTestCase


class ClientFlagRepositoryTests(BaseTestCase):

    def setUp(self):
        super(ClientFlagRepositoryTests, self).setUp()
        self.client_flag_repository = ClientFlagRepository()

    def tearDown(self):
        super(ClientFlagRepositoryTests, self).tearDown()

    def test_create(self):
        client_flag = self.client_flag_repository.create()
        self.assertIsNone(client_flag.id)
