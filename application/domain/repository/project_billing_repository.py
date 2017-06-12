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

    def create(self):
        return ProjectBilling()
