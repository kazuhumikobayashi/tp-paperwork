from application.domain.model.immutables.billing_timing import BillingTiming
from tests import BaseTestCase


class BillingTimingTests(BaseTestCase):

    def setUp(self):
        super(BillingTimingTests, self).setUp()

    def tearDown(self):
        super(BillingTimingTests, self).tearDown()

    def test_name(self):
        self.assertEqual(BillingTiming.payment_at_last.name, '契約期間末1回')
        self.assertEqual(BillingTiming.payment_by_month.name, 'その他（毎月・複数月）')

    def test_parse(self):
        payment_at_last = 1
        payment_by_month = 2

        self.assertEquals(BillingTiming.parse(payment_at_last), BillingTiming.payment_at_last)
        self.assertEquals(BillingTiming.parse(payment_by_month), BillingTiming.payment_by_month)

    def test_parse_fail_is_none(self):
        self.assertIsNone(BillingTiming.parse(0))
        self.assertIsNone(BillingTiming.parse('a'))
