from application.domain.model.order_remarks import OrderRemarks
from application.domain.repository.base_repository import BaseRepository


class OrderRemarksRepository(BaseRepository):

    model = OrderRemarks

    def create(self):
        return OrderRemarks()
