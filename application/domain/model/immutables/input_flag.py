from enum import Enum


class InputFlag(Enum):
    yet = 0
    done = 1

    @property
    def name(self):
        if self._value_ == self.yet.value:
            return '未'
        else:
            return '済'

    @property
    def payment_name(self):
        if self._value_ == self.yet.value:
            return '未払い'
        else:
            return '支払済'        

    @staticmethod
    def get_flag_for_checkbox():
        return [(str(flag.value), flag.payment_name) for flag in InputFlag]

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for flag in InputFlag:
            if flag.value == value:
                return flag
        return None

    def __str__(self):
        return str(self._value_)
