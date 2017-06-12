from application.domain.repository.project_billing_repository import ProjectBillingRepository


class ProjectBillingService(object):
    repository = ProjectBillingRepository()

    def find_by_id(self, billing_id):
        return self.repository.find_by_id(billing_id)

    def find_billings_at_a_month(self, project_id, billing_month):
        return self.repository.find_billings_at_a_month(project_id, billing_month)

    def save(self, billing):
        return self.repository.save(billing)

    def destroy(self, billing):
        return self.repository.destroy(billing)
