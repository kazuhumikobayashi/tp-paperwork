import time
from datetime import datetime, timedelta

from application.domain.model.immutables.holiday_flag import HolidayFlag
from application.domain.model.immutables.week import Week
from application.domain.repository.holiday_repository import HolidayRepository

holiday_repository = HolidayRepository()


class Calculator(object):

    # 入金・支払サイトから支払日を計算して返すメソッド
    @staticmethod
    def calculate_deposit_date_from_site(date, site):
        delta_month = (site // 30) + 1
        day = site % 30  # 0の時末月

        if day == 0:
            deposit_date = datetime.fromtimestamp(time.mktime(
                (date.year, date.month + delta_month, 1, 0, 0, 0, 0, 0, 0))) - timedelta(days=1)
        else:
            deposit_date = datetime.fromtimestamp(time.mktime(
                (date.year, date.month + delta_month, day, 0, 0, 0, 0, 0, 0)))

        return deposit_date

    # 土日の場合、前倒し・後ろ倒しした日付を返すメソッド
    @staticmethod
    def to_weekday_if_on_weekend(date, bank_holiday_flag):
        if date.weekday() == Week.saturday.value or date.weekday() == Week.sunday.value:
            # 日付を前倒し・後ろ倒しする。
            if bank_holiday_flag == HolidayFlag.before:
                date -= timedelta(days=(date.weekday() - Week.friday.value))
            else:
                next_monday = 7
                date += timedelta(days=(next_monday - date.weekday()))

        return date

    # 祝日の場合、前倒し・後ろ倒しした日付を返すメソッド
    @staticmethod
    def to_weekday_if_on_holiday(date, bank_holiday_flag):
        while holiday_repository.is_holiday(date):
            # 日付を前倒し・後ろ倒しする
            date += timedelta(days=bank_holiday_flag.value)

            # 前倒し・後ろ倒しした結果、土日になった場合はさらに前倒し・後ろ倒しにする。
            date = Calculator.to_weekday_if_on_weekend(date, bank_holiday_flag)

        return date
