import unittest

from application.domain.model.immutables.output_type import OutputType


class OutputTypeTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(OutputType.project_list.name, '案件一覧')
        self.assertEqual(OutputType.billing_list.name, '請求一覧')
        self.assertEqual(OutputType.payment_list.name, '支払一覧')
        self.assertEqual(OutputType.yayoi_interface.name, '弥生I/Fファイル')

    def test_str(self):
        project_list = '1'
        billing_list = '2'
        payment_list = '3'
        yayoi_interface = '4'

        self.assertEqual(str(OutputType.project_list), project_list)
        self.assertEqual(str(OutputType.billing_list), billing_list)
        self.assertEqual(str(OutputType.payment_list), payment_list)
        self.assertEqual(str(OutputType.yayoi_interface), yayoi_interface)
