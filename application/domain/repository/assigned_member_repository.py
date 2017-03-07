from application.domain.model.assigned_members import AssignedMember
from application.domain.repository.base_repository import BaseRepository


class AssignedMemberRepository(BaseRepository):

    model = AssignedMember

    def create(self):
        return AssignedMember()
