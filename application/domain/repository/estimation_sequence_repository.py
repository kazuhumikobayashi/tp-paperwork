from application import db
from application.domain.model.estimation_sequence import EstimationSequence
from application.domain.repository.base_repository import BaseRepository


class EstimationSequenceRepository(BaseRepository):

    model = EstimationSequence

    def find_by_fiscal_year(self, fiscal_year):
        estimation_sequence = self.model.query.filter(self.model.fiscal_year == fiscal_year).first()
        if estimation_sequence is None:
            estimation_sequence = EstimationSequence()
            estimation_sequence.fiscal_year = fiscal_year
        return estimation_sequence

    def take_a_sequence(self, fiscal_year):
        ret = self.model.query.filter(self.model.fiscal_year == fiscal_year).update(
            {'sequence': self.model.sequence + 1}
        )

        if ret == 0:
            estimation_sequence = EstimationSequence()
            estimation_sequence.fiscal_year = fiscal_year
            self.save(estimation_sequence)
        else:
            db.session.commit()
            estimation_sequence = self.find_by_fiscal_year(fiscal_year)
        return estimation_sequence

    def create(self):
        return EstimationSequence()
