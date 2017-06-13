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

    def get_project_payment_form(self, project_id):
        project_payment_forms = self.repository.get_project_payment_form(project_id)
        for project_payment_form in project_payment_forms:
            self.result_repository.get_project_payments(project_payment_form)
        return project_payment_forms

    def find_by_id(self, project_month_id):
        return self.repository.find_by_id(project_month_id)

    def find_project_month_at_a_month(self, project_id, project_month):
        return self.repository.find_project_month_at_a_month(project_id, project_month)

    def find_incomplete_results(self):
        return self.repository.find_incomplete_results()

    def find_incomplete_billings(self):
        return self.repository.find_incomplete_billings()

    def find_incomplete_deposits(self):
        return self.repository.find_incomplete_deposits()

    def save(self, project_month):
        return self.repository.save(project_month)
