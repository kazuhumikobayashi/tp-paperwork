from application.domain.model.assigned_members import AssignedMember
from application.domain.repository.base_repository import BaseRepository


class AssignedMemberRepository(BaseRepository):

    model = AssignedMember

    def find(self, page, project_id, engineer_id):
        query = self.model.query
        if project_id:
            query = query.filter(self.model.project_id.in_(project_id))
        if engineer_id:
            query = query.filter(self.model.engineer_id.in_(engineer_id))
        pagination = query.paginate(page, self.model.PER_PAGE)
        return pagination

    def create(self):
        return AssignedMember()
