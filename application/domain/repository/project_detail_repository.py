from datetime import datetime

from flask import session

from application.domain.model.immutables.status import Status
from application.domain.model.project_billing import ProjectBilling
from application.domain.model.project_detail import ProjectDetail
from application.domain.model.project_result import ProjectResult
from application.domain.repository.base_repository import BaseRepository


class ProjectDetailRepository(BaseRepository):

    model = ProjectDetail

    def save(self, project_detail):
        if project_detail.project.status == Status.done and project_detail.project.has_not_project_results\
                and project_detail.project.has_not_project_billings and project_detail.project.has_not_project_months:

            contract_dates = project_detail.project.get_project_month_list()
            for date in contract_dates:
                project_result = ProjectResult(
                                    result_month=date,
                                    created_at=datetime.today(),
                                    created_user=session['user']['user_name'],
                                    updated_at=datetime.today(),
                                    updated_user=session['user']['user_name'])
                project_detail.project_results.append(project_result)

                project_billing = ProjectBilling(
                                    billing_month=date,
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
