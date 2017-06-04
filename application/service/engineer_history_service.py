from application.domain.repository.engineer_history_repository import EngineerHistoryRepository


class EngineerHistoryService(object):
    repository = EngineerHistoryRepository()

    def find_by_id(self, engineer_history_id):
        return self.repository.find_by_id(engineer_history_id)

    def find_by_engineer_id(self, engineer_id):
        return self.repository.find_by_engineer_id(engineer_id)

    def get_latest_history(self, engineer_id):
        return self.repository.get_latest_history(engineer_id)

    def get_current_history(self, engineer_id):
        return self.repository.get_current_history(engineer_id)

    def save(self, engineer_history):
        return self.repository.save(engineer_history)

    def destroy(self, engineer_history):
        return self.repository.destroy(engineer_history)
