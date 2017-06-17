import unittest

from application.domain.model.immutables.contract import Contract


class ContractTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Contract.blanket.name, '請負契約（一括契約）')
        self.assertEqual(Contract.time_and_material.name, '準委任契約')
        self.assertEqual(Contract.dispatch.name, '派遣契約')

    def test_parse(self):
        blanket = 1
        time_and_material = 2
        dispatch = 3

        self.assertEquals(Contract.parse(blanket), Contract.blanket)
        self.assertEquals(Contract.parse(time_and_material), Contract.time_and_material)
        self.assertEquals(Contract.parse(dispatch), Contract.dispatch)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Contract.parse(0))
        self.assertIsNone(Contract.parse('a'))
