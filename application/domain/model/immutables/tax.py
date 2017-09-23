from enum import Enum


class Tax(Enum):
    zero = 0
    eight = 8
    ten = 10

    @property
    def name(self):
        if self._value_ == self.zero.value:
            return 'なし'
        elif self._value_ == self.eight.value:
            return '8％'
        else:
            return '10％'

    @property
    def rate(self):
        return self._value_ / 100

    # 税込金額から税金を割り出す
    @property
    def rate_if_exclude_tax(self):
        return self._value_ / (100 + self._value_)

    @staticmethod
    def get_type_for_select():
        ret = [('', '')]
        type_list = [(str(tax.value), tax.name) for tax in Tax]
        ret.extend(type_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for tax in Tax:
            if tax.value == value:
                return tax
        return None

    def __str__(self):
        return str(self._value_)
