from application.domain.repository.billing_repository import BillingRepository


class BillingService(object):
    repository = BillingRepository()

    def find(self, page, project_id):
        return self.repository.find(page, project_id)

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_by_id(self, billing_id):
        return self.repository.find_by_id(billing_id)

    def save(self, billing):
        return self.repository.save(billing)

    def destroy(self, billing):
        return self.repository.destroy(billing)
