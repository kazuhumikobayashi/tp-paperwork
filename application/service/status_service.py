from application.domain.repository.status_repository import StatusRepository


class StatusService(object):
    repository = StatusRepository()

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_all_for_select(self):
        ret = [('', '')]
        status_list = [(str(h.id), h.status_name) for h in self.find_all()]
        ret.extend(status_list)
        return ret

    def find_by_id(self, company_id):
        return self.repository.find_by_id(company_id)

    def save(self, company):
        return self.repository.save(company)

    def destroy(self, company):
        return self.repository.destroy(company)
