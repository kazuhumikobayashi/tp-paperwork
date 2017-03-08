from application.domain.model.billing import Billing
from application.domain.repository.base_repository import BaseRepository


class BillingRepository(BaseRepository):

    model = Billing

    def create(self):
        return Billing()
