from application.domain.model.skill import Skill
from application.domain.repository.base_repository import BaseRepository


class SkillRepository(BaseRepository):

    model = Skill

    def find(self, page, skill_name):
        query = self.model.query
        if skill_name:
            query = query.filter(self.model.skill_name.like('%' + skill_name + '%'))
        pagination = query.order_by(self.model.skill_name.asc()).paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_name(self, skill_name):
        return self.model.query.filter(self.model.skill_name == skill_name).first()

    def create(self):
        return Skill()
