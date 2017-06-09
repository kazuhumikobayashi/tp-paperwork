from application.domain.repository.project_result_repository import ProjectResultRepository


class ProjectResultService(object):
    repository = ProjectResultRepository()

    def find_incomplete_payments(self):
        return self.repository.find_incomplete_payments()
