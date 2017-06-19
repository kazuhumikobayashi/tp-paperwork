from enum import Enum


class Fraction(Enum):
    one = 1
    ten = 10
    hundred = 100
    thousand = 1000

    @property
    def name(self):
        if self._value_ == self.one.value:
            return '1円'
        elif self._value_ == self.ten.value:
            return '10円'
        elif self._value_ == self.hundred.value:
            return '100円'
        else:
            return '1000円'

    @staticmethod
    def get_fraction_for_select():
        ret = [('', '')]
        fraction_list = [(str(fraction.value), fraction.name) for fraction in Fraction]
        ret.extend(fraction_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for fraction in Fraction:
            if fraction.value == value:
                return fraction
        return None

    def __str__(self):
        return str(self._value_)
