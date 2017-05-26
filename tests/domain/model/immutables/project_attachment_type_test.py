from application.domain.model.immutables.project_attachment_type import ProjectAttachmentType
from tests import BaseTestCase


class ProjectAttachmentTypeTests(BaseTestCase):

    def setUp(self):
        super(ProjectAttachmentTypeTests, self).setUp()

    def tearDown(self):
        super(ProjectAttachmentTypeTests, self).tearDown()

    def test_name(self):
        self.assertEqual(ProjectAttachmentType.estimate.name, '見積書')
        self.assertEqual(ProjectAttachmentType.client_purchase_order.name, '顧客注文書')
        self.assertEqual(ProjectAttachmentType.bp_purchase_order.name, 'BP注文書')
        self.assertEqual(ProjectAttachmentType.order_confirmation.name, '注文請書')
        self.assertEqual(ProjectAttachmentType.client_invoice.name, '顧客請求書')
        self.assertEqual(ProjectAttachmentType.bp_invoice.name, 'BP請求書')
        self.assertEqual(ProjectAttachmentType.other.name, 'その他')

    def test_parse(self):
        estimate = 1
        client_purchase_order = 2
        bp_purchase_order = 3
        order_confirmation = 4
        client_invoice = 5
        bp_invoice = 6
        other = 9

        self.assertEquals(ProjectAttachmentType.parse(estimate), ProjectAttachmentType.estimate)
        self.assertEquals(ProjectAttachmentType.parse(client_purchase_order), ProjectAttachmentType.client_purchase_order)
        self.assertEquals(ProjectAttachmentType.parse(bp_purchase_order), ProjectAttachmentType.bp_purchase_order)
        self.assertEquals(ProjectAttachmentType.parse(order_confirmation), ProjectAttachmentType.order_confirmation)
        self.assertEquals(ProjectAttachmentType.parse(client_invoice), ProjectAttachmentType.client_invoice)
        self.assertEquals(ProjectAttachmentType.parse(bp_invoice), ProjectAttachmentType.bp_invoice)
        self.assertEquals(ProjectAttachmentType.parse(other), ProjectAttachmentType.other)

    def test_parse_fail_is_none(self):
        self.assertIsNone(ProjectAttachmentType.parse(0))
        self.assertIsNone(ProjectAttachmentType.parse('a'))
