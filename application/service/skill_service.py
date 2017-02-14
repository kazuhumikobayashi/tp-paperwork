from application.domain.repository.skill_repository import SkillRepository


class SkillService(object):
    repository = SkillRepository()

    def find(self, page, skill_name):
        return self.repository.find(page, skill_name)

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_all_for_multi_select(self):
        skill_list = [(h.id, h.skill_name) for h in self.find_all()]
        return skill_list

    def find_by_id(self, skill_id):
        return self.repository.find_by_id(skill_id)

    def save(self, skill):
        return self.repository.save(skill)

    def destroy(self, skill):
        return self.repository.destroy(skill)
