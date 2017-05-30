from application.domain.repository.company_repository import CompanyRepository


class CompanyService(object):
    repository = CompanyRepository()

    def find(self, page, company_name, client_flag_id, bank_id):
        return self.repository.find(page, company_name, client_flag_id, bank_id)

    def find_all(self, page=None):
        return self.repository.find_all(page)
    
    def find_all_for_multi_select(self):
        company_list = [(str(h.id), h.company_name) for h in self.find_all()]
        company_list.sort(key=lambda x: x[1])
        return company_list
    
    def find_for_select_by_client_flag_id(self, client_flag_id):
        ret = [('', '')]
        company_list = self.find_for_multi_select_by_client_flag_id(client_flag_id)
        ret.extend(company_list)
        return ret

    def find_for_multi_select_by_client_flag_id(self, client_flag_id):
        company_list = [(str(h.id), h.company_name) for h
                        in self.find_by_client_flag_id(client_flag_id)]
        company_list.sort(key=lambda x: x[1])
        return company_list

    def find_by_client_flag_id(self, client_flag_id):
        return self.repository.find_by_client_flag_id(client_flag_id)

    def find_by_id(self, company_id):
        return self.repository.find_by_id(company_id)

    def save(self, company):
        return self.repository.save(company)

    def destroy(self, company):
        return self.repository.destroy(company)
