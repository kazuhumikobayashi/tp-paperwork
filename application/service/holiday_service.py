from application.domain.repository.holiday_repository import HolidayRepository


class HolidayService(object):
    repository = HolidayRepository()

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_by_year(self, year):
        return self.repository.find_by_year(year)
