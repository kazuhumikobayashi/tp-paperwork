from application.domain.model.destination import Destination
from application.domain.repository.base_repository import BaseRepository


class DestinationRepository(BaseRepository):

    model = Destination

    def find(self, page, company_id, destination_name, destination_department):
        fil = self.model.query
        if company_id:
            fil = fil.filter(self.model.company_id.in_(company_id))
        if destination_name:
            fil = fil.filter(self.model.destination_name.like('%' + destination_name + '%'))
        if destination_department:
            fil = fil.filter(self.model.destination_department.like('%' + destination_department + '%'))
        pagination = fil.order_by(self.model.company_id.asc()).paginate(page, self.model.PER_PAGE)
        return pagination

    def create(self):
        return Destination()
