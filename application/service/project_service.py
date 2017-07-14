from application.domain.model.immutables.status import Status
from application.domain.repository.estimation_sequence_repository import EstimationSequenceRepository
from application.domain.repository.project_repository import ProjectRepository


class ProjectService(object):
    repository = ProjectRepository()
    estimation_sequence_repository = EstimationSequenceRepository()

    def find(self, page, project_name, status, end_user_company_id,
             client_company_id, recorded_department_id, start_date, end_date):
        return self.repository.find(page, project_name, status, end_user_company_id,
                                    client_company_id, recorded_department_id, start_date, end_date)

    def find_by_id(self, project_id):
        return self.repository.find_by_id(project_id)

    def find_incomplete_estimates(self):
        return self.repository.find_incomplete_estimates()

    def clone(self, project_id):

        project = self.find_by_id(project_id)
        project_clone = project.clone()
        project_details_clone = [detail.clone() for detail in project.project_details]
        project_clone.project_details = project_details_clone
        project_clone.status = Status.start
        project_clone.client_order_no = None

        return project_clone

    def save(self, project):
        if project.is_start_date_change:
            fiscal_year = project.get_fiscal_year()

            while True:
                estimation_sequence = self.estimation_sequence_repository.take_a_sequence(fiscal_year)
                estimation_no = estimation_sequence.get_estimation_no()

                if not self.repository.find_by_estimation_no(estimation_no):
                    project.estimation_no = estimation_no
                    break

        self.repository.save(project)

    def destroy(self, project):
        self.repository.destroy(project)
