from application.domain.model.status import Status
from application.domain.repository.base_repository import BaseRepository


class StatusRepository(BaseRepository):

    model = Status

    def find_by_name(self, status_name):
        return self.model.query.filter(self.model.status_name == status_name).first()

    def create(self):
        return Status()
