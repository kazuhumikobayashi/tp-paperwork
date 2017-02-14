from application.domain.repository.order_remarks_repository import OrderRemarksRepository


class OrderRemarksService(object):
    repository = OrderRemarksRepository()

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_by_id(self, order_remarks_id):
        return self.repository.find_by_id(order_remarks_id)

    def save(self, order_remarks):
        return self.repository.save(order_remarks)

    def destroy(self, order_remarks):
        return self.repository.destroy(order_remarks)
