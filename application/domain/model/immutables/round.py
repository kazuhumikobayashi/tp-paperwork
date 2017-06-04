from enum import Enum


class Round(Enum):
    down = 1
    up = 2
    off = 3

    @property
    def name(self):
        if self._value_ == self.down.value:
            return '切り捨て'
        elif self._value_ == self.up.value:
            return '繰り上げ'
        else:
            return '四捨五入'

    @staticmethod
    def get_round_for_select():
        ret = [('', '')]
        round_list = [(str(round_.value), round_.name) for round_ in Round]
        ret.extend(round_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for round_ in Round:
            if round_.value == value:
                return round_
        return None

    def __str__(self):
        return str(self._value_)
