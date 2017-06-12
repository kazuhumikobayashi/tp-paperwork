from application.domain.repository.project_result_repository import ProjectResultRepository


class ProjectResultService(object):
    repository = ProjectResultRepository()

    def find_by_id(self, result_id):
        return self.repository.find_by_id(result_id)

    def find_incomplete_payments(self):
        return self.repository.find_incomplete_payments()

    def save(self, project_detail):
        return self.repository.save(project_detail)
