from datetime import date

from sqlalchemy import asc

from application.domain.model.form.project_payment_form import ProjectPaymentForm
from application.domain.model.form.project_result_form import ProjectResultForm
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.project import Project
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

    def find_by_billing(self, page, project_name, result_input_flag, billing_input_flag,
                        deposit_input_flag, end_user_company_id, client_company_id,
                        recorded_department_id, deposit_date_from, deposit_date_to):
        query = self.model.query
        if project_name:
            query = query.filter(self.model.project.has(Project.project_name.like('%' + project_name + '%')))
        if result_input_flag:    
            query = query.filter(self.model.result_input_flag.
                                 in_([InputFlag.parse(st) for st in result_input_flag])) 
        if billing_input_flag:
            query = query.filter(self.model.billing_input_flag.
                                 in_([InputFlag.parse(st) for st in billing_input_flag])) 
        if deposit_input_flag:
            query = query.filter(self.model.deposit_input_flag.
                                 in_([InputFlag.parse(st) for st in deposit_input_flag])) 
        if end_user_company_id:
            query = query.filter(self.model.project.
                                 has(Project.end_user_company_id.in_(end_user_company_id)))
        if client_company_id:
            query = query.filter(self.model.project.
                                 has(Project.client_company_id.in_(client_company_id)))
        if recorded_department_id:
            query = query.filter(self.model.project.
                                 has(Project.recorded_department_id.in_(recorded_department_id)))
        if deposit_date_from:
            query = query.filter(self.model.deposit_date >= deposit_date_from)
        if deposit_date_to:
            query = query.filter(self.model.deposit_date <= deposit_date_to)
        pagination = \
            query.order_by('companies_1.company_name asc', 'companies_2.company_name asc',
                           'departments_1.department_name asc', 'projects_1.project_name asc')\
            .paginate(page, self.model.PER_PAGE)
        return pagination

    def find_project_month_at_a_month(self, project_id, project_month):
        project_month = self.model.query\
                    .filter(self.model.project_id == project_id)\
                    .filter(self.model.project_month == project_month).first()
        return project_month

    def find_by_client_billing_no(self, client_billing_no):
        return self.model.query.filter(self.model.client_billing_no == client_billing_no).first()

    def find_incomplete_results(self):
        query = self.model.query.filter(self.model.result_input_flag == InputFlag.yet)
        query = query.filter(self.model.project_month <= date.today())
        query = query.order_by(asc(self.model.project_month), asc('projects_1.project_name'))
        return query.all()

    def find_incomplete_billings(self):
        query = self.model.query.filter(self.model.billing_input_flag == InputFlag.yet)
        query = query.filter(self.model.project_month <= date.today())
        query = query.order_by(asc(self.model.project_month), asc('projects_1.project_name'))
        return query.all()

    def find_incomplete_deposits(self):
        query = self.model.query.filter(self.model.deposit_input_flag == InputFlag.yet)
        query = query.filter(self.model.deposit_date <= date.today())
        query = query.order_by(asc(self.model.deposit_date), asc('projects_1.project_name'))
        return query.all()

    def create(self):
        return ProjectMonth()
