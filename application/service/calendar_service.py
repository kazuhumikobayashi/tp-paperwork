from application.domain.repository.calendar_repository import CalendarRepository


class CalendarService(object):
    repository = CalendarRepository()

    def find_holiday_by_year(self, year):
        return self.repository.find_holiday_by_year(year)
