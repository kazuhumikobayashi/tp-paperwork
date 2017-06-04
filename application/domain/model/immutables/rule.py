from enum import Enum


class Rule(Enum):
    fixed = 1
    variable = 2

    @property
    def name(self):
        if self._value_ == self.fixed.value:
            return '固定'
        else:
            return '変動'

    @staticmethod
    def get_rule_for_select():
        ret = []
        type_list = [(str(rule.value), rule.name) for rule in Rule]
        ret.extend(type_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for rule in Rule:
            if rule.value == value:
                return rule
        return None

    def __str__(self):
        return str(self._value_)
