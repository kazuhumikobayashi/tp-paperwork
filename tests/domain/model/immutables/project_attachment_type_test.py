import unittest

from application.domain.model.immutables.project_attachment_type import ProjectAttachmentType


class ProjectAttachmentTypeTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(ProjectAttachmentType.estimate.name, '見積書')
        self.assertEqual(ProjectAttachmentType.client_purchase_order_or_invoice.name, '顧客注文書、請書')
        self.assertEqual(ProjectAttachmentType.bp_purchase_order_or_invoice.name, 'BP注文書、請書')
        self.assertEqual(ProjectAttachmentType.client_order_confirmation_or_invoice.name, '顧客請求書、納品書')
        self.assertEqual(ProjectAttachmentType.bp_order_confirmation_or_invoice.name, 'BP請求書、納品書')
        self.assertEqual(ProjectAttachmentType.other.name, 'その他')

    def test_parse(self):
        estimate = 1
        client_purchase_order_or_invoice = 2
        bp_purchase_order_or_invoice = 3
        client_order_confirmation_or_invoice = 4
        bp_order_confirmation_or_invoice = 5
        other = 9

        self.assertEquals(ProjectAttachmentType.parse(estimate), ProjectAttachmentType.estimate)
        self.assertEquals(ProjectAttachmentType.parse(client_purchase_order_or_invoice),
                          ProjectAttachmentType.client_purchase_order_or_invoice)
        self.assertEquals(ProjectAttachmentType.parse(bp_purchase_order_or_invoice),
                          ProjectAttachmentType.bp_purchase_order_or_invoice)
        self.assertEquals(ProjectAttachmentType.parse(client_order_confirmation_or_invoice),
                          ProjectAttachmentType.client_order_confirmation_or_invoice)
        self.assertEquals(ProjectAttachmentType.parse(bp_order_confirmation_or_invoice),
                          ProjectAttachmentType.bp_order_confirmation_or_invoice)
        self.assertEquals(ProjectAttachmentType.parse(other), ProjectAttachmentType.other)

    def test_parse_fail_is_none(self):
        self.assertIsNone(ProjectAttachmentType.parse(0))
        self.assertIsNone(ProjectAttachmentType.parse('a'))
