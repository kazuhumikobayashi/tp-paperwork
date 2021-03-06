from enum import Enum


class Status(Enum):
    start = 1
    placed = 2
    received = 3
    done = 4
    failure = 99

    @property
    def name(self):
        if self._value_ == self.start.value:
            return '01:契約開始'
        elif self._value_ == self.placed.value:
            return '02:発注完了'
        elif self._value_ == self.received.value:
            return '03:受注完了'
        elif self._value_ == self.done.value:
            return '04:契約完了'
        else:
            return '99:失注'

    @staticmethod
    def get_status_for_select():
        ret = [('', '')]
        type_list = Status.get_status_for_multi_select()
        ret.extend(type_list)
        return ret

    @staticmethod
    def get_status_for_multi_select():
        return [(str(status.value), status.name) for status in Status]

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for status in Status:
            if status.value == value:
                return status
        return None

    def is_done(self):
        return self == Status.done

    def __str__(self):
        return str(self._value_)
