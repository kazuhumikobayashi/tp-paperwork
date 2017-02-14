from application.domain.model.billing import Billing
from application.domain.repository.base_repository import BaseRepository


class BillingRepository(BaseRepository):

    model = Billing

    def find(self, page, project_id):
        query = self.model.query
        if project_id:
            query = query.filter(self.model.project_id.in_(project_id))
        pagination = query.paginate(page, self.model.PER_PAGE)
        return pagination

    def create(self):
        return Billing()
