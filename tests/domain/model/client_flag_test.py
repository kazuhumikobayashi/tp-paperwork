from datetime import datetime

from tests import BaseTestCase

from application.domain.model.client_flag import ClientFlag


class ClientFlagTests(BaseTestCase):

    def setUp(self):
        super(ClientFlagTests, self).setUp()

    def tearDown(self):
        super(ClientFlagTests, self).tearDown()

    def test___repr__(self):
        client_flag = ClientFlag(
                 client_flag_name='client_flag_name',
                 created_at=datetime.today(),
                 created_user='test',
                 updated_at=datetime.today(),
                 updated_user='test')

        expected = "<ClientFlag:" + \
                   "'id='{}".format(client_flag.id) + \
                   "', client_flag_name='{}".format(client_flag.client_flag_name) + \
                   "', created_at='{}".format(client_flag.created_at) + \
                   "', created_user='{}".format(client_flag.created_user) + \
                   "', updated_at='{}".format(client_flag.updated_at) + \
                   "', updated_user='{}".format(client_flag.updated_user) + \
                   "'>"
        actual = str(client_flag)
        self.assertEqual(actual, expected)
