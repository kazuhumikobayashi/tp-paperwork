from enum import Enum


class Week(Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

    @property
    def name(self):
        if self._value_ == self.monday.value:
            return '月曜日'
        if self._value_ == self.tuesday.value:
            return '火曜日'
        if self._value_ == self.wednesday.value:
            return '水曜日'
        if self._value_ == self.thursday.value:
            return '木曜日'
        if self._value_ == self.friday.value:
            return '金曜日'
        if self._value_ == self.saturday.value:
            return '土曜日'
        else:
            return '日曜日'

    @property
    def short_name(self):
        return self.name[:1]

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for week in Week:
            if week.value == value:
                return week
        return None

    def __str__(self):
        return str(self._value_)
