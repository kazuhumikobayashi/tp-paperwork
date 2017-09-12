from enum import Enum


class BillingTiming(Enum):
    billing_at_last = 1
    billing_by_month = 2

    @property
    def name(self):
        if self._value_ == self.billing_at_last.value:
            return '契約期間末1回'
        else:
            return 'その他（毎月・複数月）'

    @property
    def name_for_report(self):
        if self._value_ == self.billing_at_last.value:
            return '検収月月末締め翌月末支払い'
        else:
            return '請求毎月末締め翌月末支払い'

    @staticmethod
    def get_type_for_select():
        ret = [('', '')]
        type_list = [(str(billing_timing.value), billing_timing.name) for billing_timing in BillingTiming]
        ret.extend(type_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for billing_timing in BillingTiming:
            if billing_timing.value == value:
                return billing_timing
        return None

    def __str__(self):
        return str(self._value_)
