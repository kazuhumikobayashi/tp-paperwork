from application.domain.model.bank import Bank
from application.domain.repository.base_repository import BaseRepository


class BankRepository(BaseRepository):

    model = Bank

    def find(self, page, bank_name, text_for_document):
        query = self.model.query
        if bank_name:
            query = query.filter(self.model.bank_name.like('%' + bank_name + '%'))
        if text_for_document:
            query = query.filter(self.model.text_for_document.like('%' + text_for_document + '%'))
        pagination = query.order_by(self.model.bank_name.asc()).paginate(page, self.model.PER_PAGE)
        return pagination

    def create(self):
        return Bank()
