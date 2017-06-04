from application.domain.repository.engineer_repository import EngineerRepository


class EngineerService(object):
    repository = EngineerRepository()

    def find(self, page, engineer_name, company_id, skill_id, business_category_id):
        return self.repository.find(page, engineer_name, company_id, skill_id, business_category_id)

    def find_all_for_multi_select(self):
        engineer_list = [(str(h.id), h.engineer_name) for h in self.find_all()]
        engineer_list.sort(key=lambda x: x[1])
        return engineer_list

    def find_all_for_select(self):
        ret = [('', '')]
        engineer_list = self.find_all_for_multi_select()
        ret.extend(engineer_list)
        return ret

    def find_all(self):
        return self.repository.find_all()

    def find_by_id(self, engineer_id):
        return self.repository.find_by_id(engineer_id)

    def save(self, engineer):
        self.repository.save(engineer)

    def destroy(self, engineer):
        self.repository.destroy(engineer)
