from application.domain.model.calculation import Calculation
from application.domain.repository.base_repository import BaseRepository


class CalculationRepository(BaseRepository):

    model = Calculation

    def find(self, page, calculation_name):
        query = self.model.query
        if calculation_name:
            query = query.filter(self.model.calculation_name.like('%' + calculation_name + '%'))
        pagination = query.paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_amount_and_formula(self, amount, formula):
        query = self.model.query
        if amount:
            query = query.filter(self.model.amount == amount)
        if formula:
            query = query.filter(self.model.formula == formula)
        return query.first()

    def create(self):
        return Calculation()
