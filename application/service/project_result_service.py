from application.domain.repository.project_billing_repository import ProjectBillingRepository
from application.domain.repository.project_month_repository import ProjectMonthRepository
from application.domain.repository.project_repository import ProjectRepository
from application.domain.repository.project_result_repository import ProjectResultRepository


class ProjectResultService(object):
    project_repository = ProjectRepository()
    project_month_repository = ProjectMonthRepository()
    project_result_repository = ProjectResultRepository()
    project_billing_repository = ProjectBillingRepository()

    def find_by_id(self, result_id):
        return self.project_result_repository.find_by_id(result_id)

    def find_by_payment(self, page, project_name, estimation_no, input_flag, end_user_company_id,
                        client_company_id, recorded_department_id, engineer_name,
                        payment_expected_date_from, payment_expected_date_to):
        return self.project_result_repository.find_by_payment(page, project_name, estimation_no, input_flag,
                                                              end_user_company_id, client_company_id,
                                                              recorded_department_id, engineer_name,
                                                              payment_expected_date_from, payment_expected_date_to)

    def find_by_result(self, page, project_name, estimation_no, result_input_flag, end_user_company_id,
                       client_company_id, recorded_department_id, engineer_name, result_month_from, result_month_to):
        return self.project_result_repository.find_by_result(page, project_name, estimation_no, result_input_flag,
                                                             end_user_company_id, client_company_id,
                                                             recorded_department_id, engineer_name, result_month_from,
                                                             result_month_to)

    def find_incomplete_results(self):
        return self.project_result_repository.find_incomplete_results()

    def find_incomplete_payments(self):
        return self.project_result_repository.find_incomplete_payments()

    def save(self, result):
        if result.billing_confirmation_money:
            self.project_billing_repository.copy_and_save(result)
            project_id = result.project_detail.project_id

            # 請求明細金額と請求明細交通費を再計算する
            project = self.project_repository.find_by_id(project_id)
            billing_confirmation_money = 0
            billing_transportation = 0
            for project_detail in project.project_details:
                for project_billing in project_detail.project_billings:
                    if project_billing.billing_month == result.result_month:
                        billing_confirmation_money += project_billing.billing_confirmation_money or 0
                        billing_transportation += project_billing.billing_transportation or 0

            project_month = self.project_month_repository.find_project_month_at_a_month(project_id,
                                                                                        result.result_month)
            project_month.billing_confirmation_money = billing_confirmation_money
            project_month.billing_transportation = billing_transportation
            self.project_month_repository.save(project_month)

        return self.project_result_repository.save(result)
