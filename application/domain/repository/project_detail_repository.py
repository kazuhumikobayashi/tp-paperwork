from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.engineer import Engineer
from application.domain.model.immutables.status import Status
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.project import Project
from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.base_repository import BaseRepository


class ProjectDetailRepository(BaseRepository):

    model = ProjectDetail

    def get_project_list_our_company(self, month):
        query = self.model.query
        query = query.filter(self.model.detail_type == DetailType.engineer)
        query = query.filter(self.model.engineer
                             .has(Engineer.company
                                  .has(Company.company_client_flags
                                       .any(CompanyClientFlag.client_flag == ClientFlag.our_company))))
        query = query.filter(self.model.project.has(Project.start_date <= month))
        query = query.filter(self.model.project.has(Project.end_date >= month))
        query = query.order_by('departments_1.department_name asc', 'projects_1.estimation_no asc', 
                               'companies_2.company_name asc', 'projects_1_project_name asc',
                               'engineers_1.engineer_name asc').all()
        return query

    def get_project_list_bp(self, month):
        query = self.model.query
        query = query.filter(self.model.detail_type == DetailType.engineer)
        query = query.filter(self.model.engineer.has(Engineer.company
                                                     .has(Company.company_client_flags
                                                          .any(CompanyClientFlag.client_flag == ClientFlag.bp))))
        query = query.filter(self.model.project.has(Project.start_date <= month))
        query = query.filter(self.model.project.has(Project.end_date >= month))
        query = query.order_by('departments_1.department_name asc', 'projects_1.estimation_no asc', 
                               'companies_2.company_name asc', 'projects_1_project_name asc',
                               'engineers_1.engineer_name asc').all()
        return query

    def find_by_bp_order_no(self, bp_order_no):
        return self.model.query.filter(self.model.bp_order_no == bp_order_no).first()

    def save(self, project_detail):
        if project_detail.project.status == Status.done\
                and not project_detail.project_results and not project_detail.project_billings:

            if project_detail.is_engineer():
                project_detail.create_results()
            else:
                project_detail.create_billings()
        super(ProjectDetailRepository, self).save(project_detail)

    def destroy(self, model):
        super(ProjectDetailRepository, self).destroy(model)

    def create(self):
        return ProjectDetail()
