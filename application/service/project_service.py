from application.domain.repository.assigned_member_repository import AssignedMemberRepository
from application.domain.repository.estimation_remarks_repository import EstimationRemarksRepository
from application.domain.repository.estimation_sequence_repository import EstimationSequenceRepository
from application.domain.repository.order_remarks_repository import OrderRemarksRepository
from application.domain.repository.project_repository import ProjectRepository


class ProjectService(object):
    repository = ProjectRepository()
    assigned_member_repository = AssignedMemberRepository()
    estimation_remarks_repository = EstimationRemarksRepository()
    order_remarks_repository = OrderRemarksRepository()
    estimation_sequence_repository = EstimationSequenceRepository()

    def find(self, page, start_date, end_date, project_name, end_user_company_id, client_company_id,
             recorded_department_id):
        return self.repository.find(page, start_date, end_date, project_name, end_user_company_id, client_company_id,
                                    recorded_department_id)

    def find_by_id(self, project_id):
        return self.repository.find_by_id(project_id)

    def clone(self, project_id):

        project = self.find_by_id(project_id)
        project_clone = project.clone()
        project_clone.status_id = 1

        self.save(project_clone)
        for assigned_member in project.assigned_members:
            assigned_member_clone = assigned_member.clone()
            assigned_member_clone.project_id = project_clone.id
            self.assigned_member_repository.save(assigned_member_clone)

        if project.estimation_remarks:
            estimation_remarks_clone = project.estimation_remarks.clone()
            estimation_remarks_clone.project_id = project_clone.id
            self.estimation_remarks_repository.save(estimation_remarks_clone)

        if project.order_remarks:
            order_remarks_clone = project.order_remarks.clone()
            order_remarks_clone.project_id = project_clone.id
            self.order_remarks_repository.save(order_remarks_clone)

        return self.find_by_id(project_clone.id)

    def save(self, project):
        if project.start_date and project.is_start_date_change:
            fiscal_year = project.get_fiscal_year()
            estimation_sequence = self.estimation_sequence_repository.take_a_sequence(fiscal_year)
            project.estimation_no = estimation_sequence.get_estimation_no()
        self.repository.save(project)

    def destroy(self, project):
        self.repository.destroy(project)
