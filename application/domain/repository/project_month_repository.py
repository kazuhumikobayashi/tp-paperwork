from datetime import date

from application.domain.model.form.project_payment_form import ProjectPaymentForm
from application.domain.model.form.project_result_form import ProjectResultForm
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.project_month import ProjectMonth
from application.domain.repository.base_repository import BaseRepository


class ProjectMonthRepository(BaseRepository):

    model = ProjectMonth

    def get_project_result_form(self, project_id):
        project_months = self.model.query.order_by(self.model.project_month.desc())\
                                          .filter(self.model.project_id == project_id).all()

        return [ProjectResultForm(m.project_id, m.id, m.project_month, m.result_input_flag) for m in project_months]

    def get_project_payment_form(self, project_id):
        project_months = self.model.query.order_by(self.model.project_month.desc())\
                                          .filter(self.model.project_id == project_id).all()

        return [ProjectPaymentForm(m.project_id, m.id, m.project_month) for m in project_months]

    def find_project_month_at_a_month(self, project_id, project_month):
        project_month = self.model.query\
                    .filter(self.model.project_id == project_id)\
                    .filter(self.model.project_month == project_month).first()
        return project_month

    def find_incomplete_results(self):
        return self.model.query\
                         .filter(self.model.result_input_flag == InputFlag.yet) \
                         .filter(self.model.project_month <= date.today()).all()

    def find_incomplete_billings(self):
        return self.model.query\
                         .filter(self.model.billing_input_flag == InputFlag.yet) \
                         .filter(self.model.project_month <= date.today()).all()

    def find_incomplete_deposits(self):
        return self.model.query\
                         .filter(self.model.deposit_input_flag == InputFlag.yet) \
                         .filter(self.model.deposit_date <= date.today()).all()

    def create(self):
        return ProjectMonth()
