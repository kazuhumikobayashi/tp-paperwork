from enum import Enum


class ClientFlag(Enum):
    our_company = 1
    bp = 2
    client = 3
    end_user = 4

    @property
    def name(self):
        if self._value_ == self.our_company.value:
            return '自社'
        elif self._value_ == self.bp.value:
            return 'BP所属'
        elif self._value_ == self.client.value:
            return '顧客'
        else:
            return 'エンドユーザー'

    @staticmethod
    def get_flag_for_multi_select():
        return [(str(flag.value), flag.name) for flag in ClientFlag]

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for flag in ClientFlag:
            if flag.value == value:
                return flag
        return None

    def __str__(self):
        return str(self._value_)
