from datetime import datetime

from flask import session

from application.domain.model.immutables.status import Status
from application.domain.model.project_billing import ProjectBilling
from application.domain.model.project_detail import ProjectDetail
from application.domain.model.project_result import ProjectResult
from application.domain.repository.base_repository import BaseRepository
from application.service.calculator import Calculator


class ProjectDetailRepository(BaseRepository):

    model = ProjectDetail

    def save(self, project_detail):
        if project_detail.project.status == Status.done\
                and not project_detail.project_results and not project_detail.project_billings:

            if project_detail.is_engineer():
                # 明細がengineerの場合、明細に登録された契約期間を取得してその月々の実績レコードを作成する。
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
            else:
                # 明細がworkの場合、プロジェクト期間を取得してその月々の実績レコードを作成する。
                project_dates = project_detail.project.get_project_month_list()
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

        super(ProjectDetailRepository, self).save(project_detail)

    def destroy(self, model):
        model.billing_money = None
        super(ProjectDetailRepository, self).destroy(model)

    def create(self):
        return ProjectDetail()
