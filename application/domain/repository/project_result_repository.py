from datetime import date, timedelta

from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.engineer import Engineer
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.project import Project
from application.domain.model.project_detail import ProjectDetail
from application.domain.model.project_result import ProjectResult
from application.domain.repository.base_repository import BaseRepository


class ProjectResultRepository(BaseRepository):

    model = ProjectResult

    def get_project_results(self, project_result_form):
        project_results = self.model.query\
            .filter(self.model.project_detail.has(ProjectDetail.detail_type == DetailType.engineer))\
            .filter(self.model.project_detail.has(ProjectDetail.project_id == project_result_form.project_id))\
            .filter(self.model.result_month == project_result_form.month).all()
        project_result_form.project_results = project_results

    def get_project_payments(self, project_payment_form):
        project_results = self.model.query\
            .filter(self.model.project_detail.has(ProjectDetail.detail_type == DetailType.engineer))\
            .filter(self.model.project_detail.has(ProjectDetail.project_id == project_payment_form.project_id)) \
            .filter(self.model.project_detail.has(ProjectDetail.engineer
                                                  .has(Engineer.company
                                                       .has(Company.company_client_flags
                                                            .any(CompanyClientFlag.client_flag == ClientFlag.bp))))) \
            .filter(self.model.result_month == project_payment_form.month).all()
        project_payment_form.project_results = project_results

    def find_by_payment(self, page, project_name, input_flag, end_user_company_id,
                        client_company_id, recorded_department_id, engineer_name,
                        payment_expected_date_from, payment_expected_date_to):
        query = self.model.query\
            .filter(self.model.project_detail.has(ProjectDetail.engineer
                                                  .has(Engineer.company
                                                       .has(Company.company_client_flags
                                                            .any(CompanyClientFlag.client_flag == ClientFlag.bp))))) 
        if project_name:
            query = query.filter(self.model.project_detail.has(Project.project_name.like('%' + project_name + '%')))
        if input_flag:    
            query = query.filter(self.model.payment_flag.in_([InputFlag.parse(st) for st in input_flag])) 
        if end_user_company_id:
            query = query.filter(self.model.project_detail.has(Project.end_user_company_id.in_(end_user_company_id)))
        if client_company_id:
            query = query.filter(self.model.project_detail.has(Project.client_company_id.in_(client_company_id)))
        if recorded_department_id:
            query = query.filter(self.model.project_detail.
                                 has(Project.recorded_department_id.in_(recorded_department_id)))
        if engineer_name:
            query = query.filter(self.model.project_detail.has(Engineer.engineer_name.like('%' + engineer_name + '%')))
        if payment_expected_date_from:
            query = query.filter(self.model.payment_expected_date >= payment_expected_date_from)
        if payment_expected_date_to:
            query = query.filter(self.model.payment_expected_date <= payment_expected_date_to)
        pagination = \
            query.order_by('companies_1.company_name asc', 'companies_2.company_name asc',
                           'departments_1.department_name asc', 'engineers_1_engineer_name asc')\
            .paginate(page, self.model.PER_PAGE)
        return pagination

    def find_incomplete_payments(self):
        return self.model.query\
                     .filter(self.model.project_detail.has(ProjectDetail.detail_type == DetailType.engineer)) \
                     .filter(self.model.payment_flag == InputFlag.yet) \
                     .filter(self.model.payment_confirmation_money >= 0) \
                     .filter(self.model.payment_expected_date <= date.today() + timedelta(days=7)).all()

    def create(self):
        return ProjectResult()