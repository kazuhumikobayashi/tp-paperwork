from application.domain.repository.engineer_repository import EngineerRepository


class EngineerService(object):
    repository = EngineerRepository()

    def find(self, page, engineer_name, company_id, contract_engineer_is_checked, skill_id, business_category_id):
        return self.repository.find(page,
                                    engineer_name,
                                    company_id,
                                    contract_engineer_is_checked,
                                    skill_id,
                                    business_category_id)

    def find_contract_for_select(self):
        ret = [('', '', '')]
        engineer_list = [(str(h.id),
                          h.engineer_name + '【契約終了】' if h.is_finished_contract() else h.engineer_name,
                          h.is_finished_contract())
                         for h in self.find_all()]
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
