from application.domain.model.holiday import Holiday
from application.domain.repository.base_repository import BaseRepository


class HolidayRepository(BaseRepository):

    model = Holiday

    def find_by_year(self, year):
        return self.model.query.filter(self.model.holiday.between(year + '/1/1', year + '/12/31')).first()

    def create(self):
        return Holiday()
