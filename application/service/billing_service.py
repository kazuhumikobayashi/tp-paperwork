from application.domain.repository.billing_repository import BillingRepository


class BillingService(object):
    repository = BillingRepository()

    def find_by_id(self, billing_id):
        return self.repository.find_by_id(billing_id)

    def save(self, billing):
        return self.repository.save(billing)

    def destroy(self, billing):
        return self.repository.destroy(billing)
