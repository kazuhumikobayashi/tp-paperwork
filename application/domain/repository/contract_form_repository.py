from application.domain.model.contract_form import ContractForm
from application.domain.repository.base_repository import BaseRepository


class ContractFormRepository(BaseRepository):

    model = ContractForm

    def find_by_name(self, contract_form_name):
        return self.model.query.filter(self.model.contract_form_name == contract_form_name).first()

    def create(self):
        return ContractForm()
