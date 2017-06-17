import unittest

from application.domain.model.immutables.client_flag import ClientFlag


class ClientFlagTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(ClientFlag.our_company.name, '自社')
        self.assertEqual(ClientFlag.bp.name, 'BP所属')
        self.assertEqual(ClientFlag.client.name, '顧客')
        self.assertEqual(ClientFlag.end_user.name, 'エンドユーザー')

    def test_parse(self):
        our_company = 1
        bp = 2
        client = 3
        end_user = 4

        self.assertEquals(ClientFlag.parse(our_company), ClientFlag.our_company)
        self.assertEquals(ClientFlag.parse(bp), ClientFlag.bp)
        self.assertEquals(ClientFlag.parse(client), ClientFlag.client)
        self.assertEquals(ClientFlag.parse(end_user), ClientFlag.end_user)

    def test_parse_fail_is_none(self):
        self.assertIsNone(ClientFlag.parse(0))
        self.assertIsNone(ClientFlag.parse('a'))

    def test_str(self):
        our_company = '1'
        bp = '2'
        client = '3'
        end_user = '4'

        self.assertEqual(str(ClientFlag.our_company), our_company)
        self.assertEqual(str(ClientFlag.bp), bp)
        self.assertEqual(str(ClientFlag.client), client)
        self.assertEqual(str(ClientFlag.end_user), end_user)
