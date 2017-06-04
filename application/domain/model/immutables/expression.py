from enum import Enum


class Expression(Enum):
    more = 1
    more_than = 2
    less = 3
    less_than = 4

    @property
    def name(self):
        if self._value_ == self.more.value:
            return '以上'
        elif self._value_ == self.more_than.value:
            return 'より大きい'
        elif self._value_ == self.less.value:
            return '以下'
        else:
            return '未満'

    @staticmethod
    def get_type_for_select():
        ret = [('', '')]
        expression_list = [(str(expression.value), expression.name) for expression in Expression]
        ret.extend(expression_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for expression in Expression:
            if expression.value == value:
                return expression
        return None

    def __str__(self):
        return str(self._value_)
