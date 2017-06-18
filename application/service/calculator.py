from datetime import timedelta, date

from dateutil.relativedelta import relativedelta

from application.domain.model.immutables.holiday_flag import HolidayFlag
from application.domain.model.immutables.week import Week
from application.domain.repository.holiday_repository import HolidayRepository

holiday_repository = HolidayRepository()


class Calculator(object):

    def __init__(self, date_, site, bank_holiday_flag):
        self.date = date_
        self.site = site
        self.bank_holiday_flag = bank_holiday_flag

    # 入金予定日を計算するメソッド
    def get_deposit_date(self):
        self.calculate_deposit_date_from_site()
        self.to_weekday_if_on_weekend()
        self.to_weekday_if_on_holiday()

        return self.date

    # 入金・支払サイトから支払日を計算して返すメソッド
    def calculate_deposit_date_from_site(self):
        delta_month = (self.site.value // 30) + 1
        day = self.site.value % 30  # 0の時末月

        if self.site.is_last_day():
            self.date = date(self.date.year, self.date.month, 1) + relativedelta(months=delta_month, days=-1)
        else:
            self.date = date(self.date.year, self.date.month, day) + relativedelta(months=delta_month)

    # 土日の場合、前倒し・後ろ倒しした日付を返すメソッド
    def to_weekday_if_on_weekend(self):
        if self.date.weekday() == Week.saturday.value or self.date.weekday() == Week.sunday.value:
            # 日付を前倒し・後ろ倒しする。
            if self.bank_holiday_flag == HolidayFlag.before:
                self.date -= timedelta(days=(self.date.weekday() - Week.friday.value))
            else:
                next_monday = 7
                self.date += timedelta(days=(next_monday - self.date.weekday()))

    # 祝日の場合、前倒し・後ろ倒しした日付を返すメソッド
    def to_weekday_if_on_holiday(self):
        while holiday_repository.is_holiday(self.date):
            # 日付を前倒し・後ろ倒しする
            self.date += timedelta(days=self.bank_holiday_flag.value)

            # 前倒し・後ろ倒しした結果、土日になった場合はさらに前倒し・後ろ倒しにする。
            self.to_weekday_if_on_weekend()
