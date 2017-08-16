from enum import Enum


class Site(Enum):
    ten = 10
    twenty_five = 25
    thirty = 30
    forty = 40
    forty_five = 45
    fifty = 50
    fifty_one = 51
    fifty_five = 55
    sixty = 60

    @property
    def name(self):
        if self._value_ == self.ten.value:
            return '10'
        elif self._value_ == self.twenty_five.value:
            return '25'
        elif self._value_ == self.thirty.value:
            return '30'
        elif self._value_ == self.forty.value:
            return '40'
        elif self._value_ == self.forty_five.value:
            return '45'
        elif self._value_ == self.fifty.value:
            return '50'
        elif self._value_ == self.fifty_one.value:
            return '51'
        elif self._value_ == self.fifty_five.value:
            return '55'
        else:
            return '60'

    @staticmethod
    def get_site_for_select():
        ret = [('', '')]
        site_list = [(str(site.value), site.name) for site in Site]
        ret.extend(site_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for site in Site:
            if site.value == value:
                return site
        return None

    def is_last_day(self):
        return self._value_ % 30 == 0

    def __str__(self):
        return str(self._value_)
