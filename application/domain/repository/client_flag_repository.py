from application.domain.model.client_flag import ClientFlag
from application.domain.repository.base_repository import BaseRepository


class ClientFlagRepository(BaseRepository):

    model = ClientFlag

    def find(self, page, client_flag_name):
        query = self.model.query
        if client_flag_name:
            query = query.filter(self.model.client_flag_name.like('%' + client_flag_name + '%'))
        pagination = query.order_by(self.model.client_flag_name.asc()).paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_name(self, client_flag_name):
        return self.model.query.filter(self.model.client_flag_name == client_flag_name).first()

    def create(self):
        return ClientFlag()
