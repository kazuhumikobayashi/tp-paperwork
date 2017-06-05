from enum import Enum


class DetailType(Enum):
    engineer = 1
    work = 2

    @property
    def name(self):
        if self._value_ == self.engineer.value:
            return '技術者'
        else:
            return '作業'

    @staticmethod
    def get_type_for_select():
        ret = []
        type_list = [(str(detail_type.value), detail_type.name) for detail_type in DetailType]
        ret.extend(type_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for detail_type in DetailType:
            if detail_type.value == value:
                return detail_type
        return None

    def __str__(self):
        return str(self._value_)
