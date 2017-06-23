from application.domain.repository.order_sequence_repository import OrderSequenceRepository
from application.domain.repository.project_detail_repository import ProjectDetailRepository


class ProjectDetailService(object):
    repository = ProjectDetailRepository()
    order_sequence_repository = OrderSequenceRepository()

    def find_by_id(self, project_detail_id):
        return self.repository.find_by_id(project_detail_id)

    def save(self, project_detail):

        if project_detail.has_payment() and project_detail.is_billing_start_day_change:
            fiscal_year = project_detail.get_fiscal_year()

            while True:
                order_sequence = self.order_sequence_repository.take_a_sequence(fiscal_year)
                bp_order_no = order_sequence.get_bp_order_no()

                if not self.repository.find_by_bp_order_no(bp_order_no):
                    project_detail.bp_order_no = bp_order_no
                    break

        return self.repository.save(project_detail)

    def destroy(self, project_detail):
        return self.repository.destroy(project_detail)
