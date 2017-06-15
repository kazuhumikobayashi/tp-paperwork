from application.domain.model.project_billing import ProjectBilling
from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.base_repository import BaseRepository


class ProjectBillingRepository(BaseRepository):

    model = ProjectBilling

    def find_billings_at_a_month(self, project_id, billing_month):
        billings = self.model.query\
                    .filter(self.model.project_detail.has(ProjectDetail.project_id == project_id))\
                    .filter(self.model.billing_month == billing_month).all()
        return billings

    def copy_and_save(self, result):
        billing = self.model.query\
                      .filter(self.model.project_detail_id == result.project_detail_id)\
                      .filter(self.model.billing_month == result.result_month).first()
        if billing is None:
            billing = self.create()
            billing.project_detail_id = result.project_detail_id
            billing.billing_month = result.result_month
        billing.billing_content = result.project_detail.engineer.engineer_name
        billing.billing_amount = result.billing_confirmation_number
        billing.billing_confirmation_money = result.billing_confirmation_money
        billing.billing_transportation = result.billing_transportation
        self.save(billing)

    def create(self):
        return ProjectBilling()
