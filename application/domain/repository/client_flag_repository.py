from application.domain.model.client_flag import ClientFlag
from application.domain.repository.base_repository import BaseRepository


class ClientFlagRepository(BaseRepository):

    model = ClientFlag

    def create(self):
        return ClientFlag()
