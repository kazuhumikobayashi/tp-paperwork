from application import db
from application.domain.model.order_sequence import OrderSequence
from application.domain.repository.base_repository import BaseRepository


class OrderSequenceRepository(BaseRepository):

    model = OrderSequence

    def find_by_fiscal_year(self, fiscal_year):
        order_sequence = self.model.query.filter(self.model.fiscal_year == fiscal_year).first()
        if order_sequence is None:
            order_sequence = OrderSequence()
            order_sequence.fiscal_year = fiscal_year
        return order_sequence

    def take_a_sequence(self, fiscal_year):
        ret = self.model.query.filter(self.model.fiscal_year == fiscal_year).update(
            {'sequence': self.model.sequence + 1}
        )

        if ret == 0:
            order_sequence = OrderSequence()
            order_sequence.fiscal_year = fiscal_year
            self.save(order_sequence)
        else:
            db.session.commit()
            order_sequence = self.find_by_fiscal_year(fiscal_year)
        return order_sequence

    def create(self):
        return OrderSequence()
