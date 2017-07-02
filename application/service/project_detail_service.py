from application.domain.repository.order_sequence_repository import OrderSequenceRepository
from application.domain.repository.project_detail_repository import ProjectDetailRepository
from application.domain.repository.project_repository import ProjectRepository


class ProjectDetailService(object):
    project_repository = ProjectRepository()
    project_detail_repository = ProjectDetailRepository()
    order_sequence_repository = OrderSequenceRepository()

    def find_by_id(self, project_detail_id):
        return self.project_detail_repository.find_by_id(project_detail_id)

    def save(self, project_detail):

        if project_detail.has_payment() and project_detail.is_billing_start_day_change:
            fiscal_year = project_detail.get_fiscal_year()

            while True:
                order_sequence = self.order_sequence_repository.take_a_sequence(fiscal_year)
                bp_order_no = order_sequence.get_bp_order_no()

                if not self.project_detail_repository.find_by_bp_order_no(bp_order_no):
                    project_detail.bp_order_no = bp_order_no
                    break

        self.project_detail_repository.save(project_detail)

        # 見積金額合計を再計算する
        estimated_total_amount = 0
        project = self.project_repository.find_by_id(project_detail.project_id)
        for detail in project.project_details:
            estimated_total_amount += detail.billing_money or 0
        project.estimated_total_amount = estimated_total_amount
        self.project_repository.save(project)

    def destroy(self, project_detail):
        # 見積金額合計を再計算する
        estimated_total_amount = 0
        project = self.project_repository.find_by_id(project_detail.project_id)
        for detail in project.project_details:
            if detail.id != project_detail.id:
                estimated_total_amount += detail.billing_money or 0
        project.estimated_total_amount = estimated_total_amount
        self.project_repository.save(project)

        return self.project_detail_repository.destroy(project_detail)
