from enum import Enum


class Gender(Enum):
    male = 1
    female = 2

    @property
    def name(self):
        if self._value_ == self.male.value:
            return '男性'
        else:
            return '女性'

    @staticmethod
    def get_gender_for_radio():
        return [(str(gender.value), gender.name) for gender in Gender]

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for gender in Gender:
            if gender.value == value:
                return gender
        return None

    def __str__(self):
        return str(self._value_)
