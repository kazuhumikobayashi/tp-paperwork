from application.domain.repository.company_repository import CompanyRepository
from application.domain.repository.department_repository import DepartmentRepository
from application.domain.repository.project_result_repository import ProjectResultRepository


class PaymentListService(object):
    project_result_repository = ProjectResultRepository()
    department_repository = DepartmentRepository()
    company_repository = CompanyRepository()

    def get_payment_lists_by_department(self, month):
        payment_lists = []

        # 部署ごとにまとめたpayment_listを取得する。
        for department in self.department_repository.find_all():
            payment_list = self.project_result_repository.get_payment_list_by_department(month, department)
            payment_lists.append(payment_list)
        return payment_lists

    def get_payment_list_order_by_payment_date(self, month):
        return self.project_result_repository.get_payment_list_order_by_payment_date(month)
