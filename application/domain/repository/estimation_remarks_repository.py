from application.domain.model.estimation_remarks import EstimationRemarks
from application.domain.repository.base_repository import BaseRepository


class EstimationRemarksRepository(BaseRepository):

    model = EstimationRemarks

    def create(self):
        return EstimationRemarks()
