import unittest

from application.domain.model.immutables.billing_timing import BillingTiming


class BillingTimingTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(BillingTiming.billing_at_last.name, '契約期間末1回')
        self.assertEqual(BillingTiming.billing_by_month.name, 'その他（毎月・複数月）')

    def test_name_for_report(self):
        self.assertEqual(BillingTiming.billing_at_last.name_for_report, '納入検収後、月末締め翌月末支払')
        self.assertEqual(BillingTiming.billing_by_month.name_for_report, '請求毎月末締め翌月末払い')

    def test_parse(self):
        billing_at_last = 1
        billing_by_month = 2

        self.assertEqual(BillingTiming.parse(billing_at_last), BillingTiming.billing_at_last)
        self.assertEqual(BillingTiming.parse(billing_by_month), BillingTiming.billing_by_month)

    def test_parse_fail_is_none(self):
        self.assertIsNone(BillingTiming.parse(0))
        self.assertIsNone(BillingTiming.parse('a'))
