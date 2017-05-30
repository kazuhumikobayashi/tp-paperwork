from enum import Enum


class BillingTiming(Enum):
    payment_at_last = 1
    payment_by_month = 2

    @property
    def name(self):
        if self._value_ == self.payment_at_last.value:
            return '契約期間末1回'
        elif self._value_ == self.payment_by_month.value:
            return 'その他（毎月・複数月）'

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
