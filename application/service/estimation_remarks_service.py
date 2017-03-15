from application.domain.repository.estimation_remarks_repository import EstimationRemarksRepository


class EstimationRemarksService(object):
    repository = EstimationRemarksRepository()

    def save(self, estimation_remarks):
        return self.repository.save(estimation_remarks)
