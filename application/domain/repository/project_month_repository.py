from datetime import date

from application.domain.model.project_month import ProjectMonth
from application.domain.repository.base_repository import BaseRepository


class ProjectMonthRepository(BaseRepository):

    model = ProjectMonth

    def find_incomplete_results(self):
        return self.model.query\
                         .filter(self.model.result_input_flag == 0) \
                         .filter(self.model.project_month <= date.today()).all()

    def find_incomplete_billings(self):
        return self.model.query\
                         .filter(self.model.billing_input_flag == 0) \
                         .filter(self.model.project_month <= date.today()).all()

    def find_incomplete_deposits(self):
        return self.model.query\
                         .filter(self.model.deposit_input_flag == 0) \
                         .filter(self.model.deposit_date <= date.today()).all()
