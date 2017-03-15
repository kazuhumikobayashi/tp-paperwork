from application.domain.repository.order_remarks_repository import OrderRemarksRepository


class OrderRemarksService(object):
    repository = OrderRemarksRepository()

    def save(self, order_remarks):
        return self.repository.save(order_remarks)
