from datetime import datetime

from flask import session

from application.domain.model.immutables.status import Status
from application.domain.model.project import Project
from application.domain.model.project_billing import ProjectBilling
from application.domain.model.project_month import ProjectMonth
from application.domain.model.project_result import ProjectResult
from application.domain.repository.base_repository import BaseRepository
from application.service.calculator import Calculator


class ProjectRepository(BaseRepository):

    model = Project

    def find(self, page, project_name, status, end_user_company_id,
             client_company_id, recorded_department_id, start_date, end_date):
        query = self.model.query
        if project_name:
            query = query.filter(self.model.project_name.like('%' + project_name + '%'))
        if status:    
            query = query.filter(self.model.status.in_([Status.parse(st) for st in status]))         
        if end_user_company_id:
            query = query.filter(self.model.end_user_company_id.in_(end_user_company_id))
        if client_company_id:
            query = query.filter(self.model.client_company_id.in_(client_company_id))
        if recorded_department_id:
            query = query.filter(self.model.recorded_department_id.in_(recorded_department_id))
        if start_date:
            query = query.filter(self.model.start_date >= start_date)
        if end_date:
            query = query.filter(self.model.end_date <= end_date)
        pagination = \
            query.order_by('companies_1.company_name asc', 'companies_2.company_name asc',
                           'departments_1.department_name asc', self.model.project_name.asc())\
            .paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_estimation_no(self, estimation_no):
        return self.model.query.filter(self.model.estimation_no == estimation_no).first()

    def find_incomplete_estimates(self):
        return self.model.query.filter(self.model.status <= Status.received).all()

    def save(self, project):
        if project.status == Status.done and project.has_not_project_results() and project.has_not_project_billings()\
                and project.has_not_project_months():

            project_dates = project.get_project_month_list()
            for date in project_dates:
                calculator = Calculator(
                                date,
                                project.client_company.billing_site,
                                project.client_company.bank_holiday_flag)
                project_month = ProjectMonth(
                                        project_month=date,
                                        deposit_date=calculator.get_deposit_date(),
                                        created_at=datetime.today(),
                                        created_user=session['user']['user_name'],
                                        updated_at=datetime.today(),
                                        updated_user=session['user']['user_name'])
                project.project_months.append(project_month)

            for project_detail in project.project_details:
                # 明細がengineerの場合、明細に登録された契約期間を取得してその月々の実績レコードを作成する。
                if project_detail.is_engineer():
                    contract_dates = project_detail.get_contract_month_list()
                    for date in contract_dates:
                        project_result = ProjectResult(
                                            result_month=date,
                                            created_at=datetime.today(),
                                            created_user=session['user']['user_name'],
                                            updated_at=datetime.today(),
                                            updated_user=session['user']['user_name'])
                        if project_detail.has_payment():
                            calculator = Calculator(
                                            date,
                                            project_detail.engineer.company.payment_site,
                                            project_detail.get_holiday_flag_if_payment())
                            project_result.payment_expected_date = calculator.get_deposit_date()
                        project_detail.project_results.append(project_result)
                # 明細がworkの場合、プロジェクト期間を取得してその月々の実績レコードを作成する。
                else:
                    for date in project_dates:
                        project_billing = ProjectBilling(
                                            billing_month=date,
                                            billing_content=project_detail.work_name,
                                            billing_confirmation_money=project_detail.get_payment_per_month_by_work(),
                                            created_at=datetime.today(),
                                            created_user=session['user']['user_name'],
                                            updated_at=datetime.today(),
                                            updated_user=session['user']['user_name'])
                        project_detail.project_billings.append(project_billing)

        super(ProjectRepository, self).save(project)

    def create(self):
        return Project()
