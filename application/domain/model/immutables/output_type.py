from enum import Enum


class OutputType(Enum):
    project_list = 1
    billing_list = 2
    payment_list = 3
    yayoi_interface = 4

    @property
    def name(self):
        if self._value_ == self.project_list.value:
            return '案件一覧'
        elif self._value_ == self.billing_list.value:
            return '請求一覧'
        elif self._value_ == self.payment_list.value:
            return '支払一覧'
        else:
            return '弥生I/Fファイル'

    @staticmethod
    def get_type_for_select():
        ret = [('', '')]
        type_list = [(str(output_type.value), output_type.name) for output_type in OutputType]
        ret.extend(type_list)
        return ret

    def __str__(self):
        return str(self._value_)
