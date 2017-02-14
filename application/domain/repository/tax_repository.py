from application.domain.model.tax import Tax
from application.domain.repository.base_repository import BaseRepository


class TaxRepository(BaseRepository):

    model = Tax

    def find(self, page, tax_rate):
        query = self.model.query
        if tax_rate:
            query = query.filter(self.model.tax_rate == tax_rate)
        pagination = query.paginate(page, self.model.PER_PAGE)
        return pagination

    def create(self):
        return Tax()
