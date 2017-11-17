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

    def find_by_id(self, engineer_id):
        return self.repository.find_by_id(engineer_id)

    def save(self, engineer):
        self.repository.save(engineer)

    def destroy(self, engineer):
        self.repository.destroy(engineer)
