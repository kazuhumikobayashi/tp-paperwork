from application import db
from application.domain.model.billing_sequence import BillingSequence
from application.domain.model.estimation_sequence import EstimationSequence
from application.domain.repository.base_repository import BaseRepository


class BillingSequenceRepository(BaseRepository):

    model = BillingSequence

    def find_by_fiscal_year(self, fiscal_year):
        billing_sequence = self.model.query.filter(self.model.fiscal_year == fiscal_year).first()
        if billing_sequence is None:
            billing_sequence = BillingSequence()
            billing_sequence.fiscal_year = fiscal_year
        return billing_sequence

    def take_a_sequence(self, fiscal_year):
        ret = self.model.query.filter(self.model.fiscal_year == fiscal_year).update(
            {'sequence': self.model.sequence + 1}
        )

        if ret == 0:
            billing_sequence = BillingSequence()
            billing_sequence.fiscal_year = fiscal_year
            self.save(billing_sequence)
        else:
            db.session.commit()
            billing_sequence = self.find_by_fiscal_year(fiscal_year)
        return billing_sequence

    def create(self):
        return BillingSequence()
