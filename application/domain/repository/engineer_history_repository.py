from datetime import datetime

from application.domain.model.engineer_history import EngineerHistory
from application.domain.repository.base_repository import BaseRepository


class EngineerHistoryRepository(BaseRepository):

    model = EngineerHistory

    def find_by_engineer_id(self, engineer_id):
        fil = self.model.query
        engineer_histories = fil.order_by(self.model.receipt_start_day).filter(
            self.model.engineer_id == engineer_id).all()
        return engineer_histories

    def get_latest_history(self, engineer_id):
        fil = self.model.query
        latest_engineer_history = fil.order_by(self.model.receipt_start_day.desc()).filter(
            self.model.engineer_id == engineer_id).first()
        if latest_engineer_history is None:
            latest_engineer_history = self.create()
        return latest_engineer_history

    def get_current_history(self, engineer_id):
        fil = self.model.query
        current_engineer_history = fil.filter(self.model.engineer_id == engineer_id,
                                              self.model.receipt_start_day <= datetime.now().date(),
                                              datetime.now().date() <= self.model.receipt_end_day
                                              ).first()
        if current_engineer_history is None:
            current_engineer_history = self.create()
        return current_engineer_history

    def create(self):
        return EngineerHistory()
