from application.domain.repository.estimation_remarks_repository import EstimationRemarksRepository


class EstimationRemarksService(object):
    repository = EstimationRemarksRepository()

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_by_id(self, estimation_remarks_id):
        return self.repository.find_by_id(estimation_remarks_id)

    def save(self, estimation_remarks):
        return self.repository.save(estimation_remarks)

    def destroy(self, estimation_remarks):
        return self.repository.destroy(estimation_remarks)
