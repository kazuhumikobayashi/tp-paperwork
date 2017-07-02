from application.domain.repository.project_billing_repository import ProjectBillingRepository
from application.domain.repository.project_month_repository import ProjectMonthRepository
from application.domain.repository.project_repository import ProjectRepository


class ProjectBillingService(object):
    project_billing_repository = ProjectBillingRepository()
    project_month_repository = ProjectMonthRepository()
    project_repository = ProjectRepository()

    def find_by_id(self, billing_id):
        return self.project_billing_repository.find_by_id(billing_id)

    def find_billings_at_a_month(self, project_id, billing_month):
        return self.project_billing_repository.find_billings_at_a_month(project_id, billing_month)

    def save(self, billing):
        self.project_billing_repository.save(billing)
        project_id = billing.project_detail.project_id

        # 請求明細金額と請求明細交通費を再計算する
        project = self.project_repository.find_by_id(project_id)
        billing_confirmation_money = 0
        billing_transportation = 0
        for project_detail in project.project_details:
            for project_billing in project_detail.project_billings:
                if project_billing.billing_month == billing.billing_month:
                    billing_confirmation_money += project_billing.billing_confirmation_money or 0
                    billing_transportation += project_billing.billing_transportation or 0

        project_month = self.project_month_repository.find_project_month_at_a_month(project_id, billing.billing_month)
        project_month.billing_confirmation_money = billing_confirmation_money
        project_month.billing_transportation = billing_transportation
        self.project_month_repository.save(project_month)

    def destroy(self, billing):
        return self.project_billing_repository.destroy(billing)
