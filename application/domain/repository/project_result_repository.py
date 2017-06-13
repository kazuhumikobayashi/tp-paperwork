from datetime import date, timedelta

from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.engineer import Engineer
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.input_flag import InputFlag
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

    def find_incomplete_payments(self):
        return self.model.query\
                     .filter(self.model.project_detail.has(ProjectDetail.detail_type == DetailType.engineer)) \
                     .filter(self.model.payment_flag == InputFlag.yet) \
                     .filter(self.model.payment_confirmation_money >= 0) \
                     .filter(self.model.payment_expected_date <= date.today() + timedelta(days=7)).all()

    def create(self):
        return ProjectResult()
