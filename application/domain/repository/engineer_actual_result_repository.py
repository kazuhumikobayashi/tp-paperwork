from application.domain.model.engineer_actual_result import EngineerActualResult
from application.domain.repository.base_repository import BaseRepository


class EngineerActualResultRepository(BaseRepository):

    model = EngineerActualResult

    def create(self):
        return EngineerActualResult()
