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

    def clone(self, project_id):

        project = self.find_by_id(project_id)
        project_clone = project.clone()
        project_clone.status_id = Status.start

        self.save(project_clone)

        return self.find_by_id(project_clone.id)

    def save(self, project):
        if project.is_start_date_change:
            fiscal_year = project.get_fiscal_year()
            estimation_sequence = self.estimation_sequence_repository.take_a_sequence(fiscal_year)
            project.estimation_no = estimation_sequence.get_estimation_no()
        self.repository.save(project)

    def destroy(self, project):
        self.repository.destroy(project)
