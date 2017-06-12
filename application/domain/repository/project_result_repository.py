from datetime import date, timedelta

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

    def find_incomplete_payments(self):
        return self.model.query\
                     .filter(self.model.project_detail.has(ProjectDetail.detail_type == DetailType.engineer)) \
                     .filter(self.model.payment_flag == InputFlag.yet) \
                     .filter(self.model.payment_confirmation_money >= 0) \
                     .filter(self.model.payment_expected_date <= date.today() + timedelta(days=7)).all()

    def create(self):
        return ProjectResult()
