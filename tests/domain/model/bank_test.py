from application.domain.model.bank import Bank
from tests import BaseTestCase
from datetime import datetime


class BankTests(BaseTestCase):

    def setUp(self):
        super(BankTests, self).setUp()

    def tearDown(self):
        super(BankTests, self).tearDown()

    def test___repr__(self):
        bank = Bank(
                 bank_name='bank_name',
                 text_for_document='text_for_document',
                 created_at=datetime.today(),
                 created_user='test',
                 updated_at=datetime.today(),
                 updated_user='test')

        expected = "<Bank:" + \
                "'id='{}".format(bank.id) + \
                "', bank_name='{}".format(bank.bank_name) + \
                "', text_for_document='{}".format(bank.text_for_document) + \
                "', created_at='{}".format(bank.created_at) + \
                "', created_user='{}".format(bank.created_user) + \
                "', updated_at='{}".format(bank.updated_at) + \
                "', updated_user='{}".format(bank.updated_user) + \
                "'>"
        actual = str(bank)
        self.assertEqual(actual, expected)
