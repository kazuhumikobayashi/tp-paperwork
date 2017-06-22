from application.domain.repository.project_billing_repository import ProjectBillingRepository
from application.domain.repository.project_result_repository import ProjectResultRepository


class ProjectResultService(object):
    repository = ProjectResultRepository()
    billing_repository = ProjectBillingRepository()

    def find_by_id(self, result_id):
        return self.repository.find_by_id(result_id)

    def find_by_payment(self, page, project_name, input_flag, end_user_company_id,
                        client_company_id, recorded_department_id, engineer_name,
                        payment_expected_date_from, payment_expected_date_to):
        return self.repository.find_by_payment(page, project_name, input_flag, end_user_company_id,
                                               client_company_id, recorded_department_id, engineer_name,
                                               payment_expected_date_from, payment_expected_date_to)

    def find_incomplete_payments(self):
        return self.repository.find_incomplete_payments()

    def save(self, result):
        if result.billing_confirmation_money:
            self.billing_repository.copy_and_save(result)

        return self.repository.save(result)
