from enum import Enum


class HolidayFlag(Enum):
    before = -1
    after = 1

    @property
    def name(self):
        if self._value_ == self.before.value:
            return '前倒し'
        else:
            return '後ろ倒し'

    @staticmethod
    def get_flag_for_radio():
        return [(str(flag.value), flag.name) for flag in HolidayFlag]

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for flag in HolidayFlag:
            if flag.value == value:
                return flag
        return None

    def __str__(self):
        return str(self._value_)
