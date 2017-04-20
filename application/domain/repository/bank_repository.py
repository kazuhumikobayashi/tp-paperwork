from application.domain.model.bank import Bank
from application.domain.repository.base_repository import BaseRepository


class BankRepository(BaseRepository):

    model = Bank

    def create(self):
        return Bank()
