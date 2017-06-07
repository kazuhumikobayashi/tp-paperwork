from application.domain.model.holiday import Holiday
from application.domain.repository.base_repository import BaseRepository


class HolidayRepository(BaseRepository):

    model = Holiday

    def find_by_year(self, year, page):
        fil = self.model.query
        if year:
            fil = fil.filter(self.model.holiday.between(year + '/1/1', year + '/12/31'))
        if page:
            return fil.order_by(self.model.holiday.asc()).paginate(page, self.model.PER_PAGE)
        else:
            return fil.order_by(self.model.holiday.asc()).all()

    def find_by_date(self, date):
        return self.model.query.filter(self.model.holiday == date).first()

    def is_holiday(self, date):
        fil = self.model.query
        fil = fil.filter(self.model.holiday == date).first()
        return True if fil else False

    def create(self):
        return Holiday()
