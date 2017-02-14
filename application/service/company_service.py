from application.domain.repository.company_repository import CompanyRepository


class CompanyService(object):
    repository = CompanyRepository()

    def find(self, page, company_name, company_code):
        return self.repository.find(page, company_name, company_code)

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_all_for_select(self):
        ret = [('', '')]
        company_list = self.find_all_for_multi_select()
        ret.extend(company_list)
        return ret

    def find_all_for_multi_select(self):
        company_list = [(str(h.id), h.company_name) for h in self.find_all()]
        return company_list

    def find_by_id(self, company_id):
        return self.repository.find_by_id(company_id)

    def save(self, company):
        return self.repository.save(company)

    def destroy(self, company):
        return self.repository.destroy(company)
