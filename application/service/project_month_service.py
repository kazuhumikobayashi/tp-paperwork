from application.domain.repository.project_month_repository import ProjectMonthRepository
from application.domain.repository.project_result_repository import ProjectResultRepository


class ProjectMonthService(object):
    repository = ProjectMonthRepository()
    result_repository = ProjectResultRepository()

    def get_project_result_form(self, project_id):
        project_result_forms = self.repository.get_project_result_form(project_id)
        for project_result_form in project_result_forms:
            self.result_repository.get_project_results(project_result_form)
        return project_result_forms

    def find_incomplete_results(self):
        return self.repository.find_incomplete_results()

    def find_incomplete_billings(self):
        return self.repository.find_incomplete_billings()

    def find_incomplete_deposits(self):
        return self.repository.find_incomplete_deposits()
