from application.domain.repository.contract_form_repository import ContractFormRepository


class ContractFormService(object):
    repository = ContractFormRepository()

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_all_for_select(self):
        ret = [('', '')]
        contract_form_list = self.find_all_for_multi_select()
        ret.extend(contract_form_list)
        return ret

    def find_all_for_multi_select(self):
        contract_form_list = [(str(h.id), h.contract_form_name) for h in self.find_all()]
        return contract_form_list
