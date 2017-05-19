from application.domain.repository.holiday_repository import HolidayRepository


class HolidayService(object):
    repository = HolidayRepository()

    def find_by_year(self, year, page=None):
        return self.repository.find_by_year(year, page)

    def find_by_id(self, holiday_id):
        return self.repository.find_by_id(holiday_id)

    def save(self, holiday):
        if isinstance(holiday, list):
            for data in holiday:
                self.repository.save(data)
        else:
            return self.repository.save(holiday)

    def destroy(self, holiday):
        return self.repository.destroy(holiday)
