from enum import Enum


class Contract(Enum):
    blanket = 1
    time_and_material = 2
    dispatch = 3

    @property
    def name(self):
        if self._value_ == self.blanket.value:
            return '請負契約（一括契約）'
        elif self._value_ == self.time_and_material.value:
            return '準委任契約'
        else:
            return '派遣契約'

    @staticmethod
    def get_type_for_select():
        ret = [('', '')]
        type_list = [(str(contract.value), contract.name) for contract in Contract]
        ret.extend(type_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for contract in Contract:
            if contract.value == value:
                return contract
        return None

    def __str__(self):
        return str(self._value_)
