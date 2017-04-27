from application.domain.repository.bank_repository import BankRepository


class BankService(object):
    repository = BankRepository()

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_all_for_select(self):
        ret = [('', '')]
        bank_list = self.find_all_for_multi_select()
        ret.extend(bank_list)
        return ret

    def find_all_for_multi_select(self):
        bank_list = [(str(h.id), h.bank_name) for h in self.find_all()]
        return bank_list
