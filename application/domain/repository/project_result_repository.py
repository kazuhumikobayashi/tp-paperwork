from datetime import date, timedelta, datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import asc, or_

from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.engineer import Engineer
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.project import Project
from application.domain.model.project_detail import ProjectDetail
from application.domain.model.project_result import ProjectResult
from application.domain.model.report.payment_list_by_department import PaymentListByDepartment
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

    def find_by_payment(self, page, project_name, estimation_no, input_flag, end_user_company_id,
                        client_company_id, recorded_department_id, engineer_name,
                        payment_expected_date_from, payment_expected_date_to):
        query = self.model.query\
            .filter(self.model.project_detail.has(ProjectDetail.engineer
                                                  .has(Engineer.company
                                                       .has(Company.company_client_flags
                                                            .any(CompanyClientFlag.client_flag == ClientFlag.bp)))))
        if project_name:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project.has(Project.project_name.like('%' + project_name + '%'))))
        if estimation_no:
            cut_space_of_estimation_no = estimation_no.replace(' ', ',').replace('　', ',')
            estimation_no_list = [estimation_no.strip() for estimation_no in cut_space_of_estimation_no.split(',')
                                  if not estimation_no.strip() == '']
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project
                                      .has(or_(*[Project.estimation_no.like('%' + estimation_no + '%')
                                                 for estimation_no in estimation_no_list]))))
        if input_flag:
            query = query.filter(self.model.payment_flag.in_([InputFlag.parse(st) for st in input_flag]))
        if end_user_company_id:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project.has(Project.end_user_company_id.in_(end_user_company_id))))
        if client_company_id:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project.has(Project.client_company_id.in_(client_company_id))))
        if recorded_department_id:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project
                                      .has(Project.recorded_department_id.in_(recorded_department_id))))
        if engineer_name:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.engineer
                                      .has(Engineer.engineer_name.like('%' + engineer_name + '%'))))
        if payment_expected_date_from:
            query = query.filter(self.model.payment_expected_date >= payment_expected_date_from)
        if payment_expected_date_to:
            query = query.filter(self.model.payment_expected_date <= payment_expected_date_to)
        pagination = \
            query.order_by('companies_1.company_name asc', 'companies_2.company_name asc',
                           'departments_1.department_name asc', 'engineers_1_engineer_name asc',
                           asc(self.model.payment_expected_date))\
            .paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_result(self, page, project_name, estimation_no, result_input_flag, end_user_company_id,
                       client_company_id, recorded_department_id, engineer_name, result_month_from, result_month_to):
        query = self.model.query\
            .filter(self.model.project_detail.has(ProjectDetail.detail_type == DetailType.engineer))
        if project_name:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project.has(Project.project_name.like('%' + project_name + '%'))))
        if estimation_no:
            cut_space_of_estimation_no = estimation_no.replace(' ', ',').replace('　', ',')
            estimation_no_list = [estimation_no.strip() for estimation_no in cut_space_of_estimation_no.split(',')
                                  if not estimation_no.strip() == '']
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project
                                      .has(or_(*[Project.estimation_no.like('%' + estimation_no + '%')
                                                 for estimation_no in estimation_no_list]))))
        if result_input_flag and len(result_input_flag) == 1:
            if InputFlag.yet in [InputFlag.parse(f) for f in result_input_flag]:
                query = query.filter(or_(self.model.work_time == 0, self.model.work_time.is_(None)))
            if InputFlag.done in [InputFlag.parse(f) for f in result_input_flag]:
                query = query.filter(self.model.work_time > 0)
        if end_user_company_id:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project.has(Project.end_user_company_id.in_(end_user_company_id))))
        if client_company_id:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project.has(Project.client_company_id.in_(client_company_id))))
        if recorded_department_id:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.project
                                      .has(Project.recorded_department_id.in_(recorded_department_id))))
        if engineer_name:
            query = query.filter(self.model.project_detail
                                 .has(ProjectDetail.engineer
                                      .has(Engineer.engineer_name.like('%' + engineer_name + '%'))))
        if result_month_from:
            tmp_data = datetime.strptime(result_month_from, '%Y/%m').date()
            result_month_from = date(tmp_data.year, tmp_data.month, 1)

            query = query.filter(self.model.result_month >= result_month_from)
        if result_month_to:
            tmp_data = datetime.strptime(result_month_to, '%Y/%m').date()
            result_month_to = tmp_data + relativedelta(months=1, days=-1)

            query = query.filter(self.model.result_month <= result_month_to)
        pagination = \
            query.order_by('companies_1.company_name asc', 'companies_2.company_name asc',
                           'departments_1.department_name asc', 'engineers_1_engineer_name asc',
                           asc(self.model.result_month))\
            .paginate(page, self.model.PER_PAGE)
        return pagination

    def get_payment_list_by_department(self, month, department):
        query = self.model.query
        # BPの実績のみ取得
        query = query.filter(self.model.project_detail
                             .has(ProjectDetail.engineer
                                  .has(Engineer.company
                                       .has(Company.company_client_flags
                                            .any(CompanyClientFlag.client_flag == ClientFlag.bp)))))
        # 指定した月の実績を取得
        query = query.filter(self.model.result_month == month)
        # 指定の部署に所属しているBPに絞り込む
        query = query.filter(self.model.project_detail
                             .has(ProjectDetail.project
                                  .has(Project.recorded_department_id == department.id)))

        # プロジェクト名称の降順にする。
        query = query.join(self.model.project_detail)\
                     .join(ProjectDetail.project)\
                     .order_by(Project.client_company_id.asc(), Project.project_name.asc())

        project_results = query.all()

        payment_list = PaymentListByDepartment(
                                    month=month,
                                    department=department,
                                    project_results=project_results)
        return payment_list

    def get_payment_list_order_by_payment_date(self, month):
        query = self.model.query
        # BPの実績のみ取得
        query = query.filter(self.model.project_detail
                             .has(ProjectDetail.engineer
                                  .has(Engineer.company
                                       .has(Company.company_client_flags
                                            .any(CompanyClientFlag.client_flag == ClientFlag.bp)))))
        # 指定した月の実績を取得。
        query = query.filter(self.model.result_month == month)
        # 支払日の昇順にする。
        query = query.order_by(self.model.payment_expected_date.asc())

        payment_list = query.all()

        return payment_list

    def find_incomplete_results(self):
        today = datetime.today().date()
        first_day = today.replace(day=1)
        last_first_day = first_day + relativedelta(months=-1)

        query = self.model.query.filter(self.model.project_detail.has(ProjectDetail.detail_type == DetailType.engineer))
        query = query.filter(or_(self.model.work_time == 0, self.model.work_time.is_(None)))
        query = query.filter(self.model.result_month <= last_first_day)
        query = query.order_by(asc(self.model.result_month), asc('projects_1.project_name'))
        return query.all()

    def find_incomplete_payments(self):
        query = self.model.query.filter(self.model.project_detail.has(ProjectDetail.detail_type == DetailType.engineer))
        query = query.filter(self.model.payment_flag == InputFlag.yet)
        query = query.filter(self.model.payment_confirmation_money > 0)
        query = query.filter(self.model.payment_expected_date <= date.today() + timedelta(days=7))
        query = query.order_by(asc(self.model.payment_expected_date), asc('projects_1.project_name'))
        return query.all()

    def create(self):
        return ProjectResult()
