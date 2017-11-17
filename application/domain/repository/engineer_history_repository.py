from application.domain.model.engineer_history import EngineerHistory
from application.domain.repository.base_repository import BaseRepository


class EngineerHistoryRepository(BaseRepository):

    model = EngineerHistory

    def find_by_engineer_id(self, engineer_id):
        fil = self.model.query
        engineer_histories = fil.order_by(self.model.payment_start_day).filter(
            self.model.engineer_id == engineer_id).all()
        return engineer_histories

    def get_latest_history(self, engineer_id):
        fil = self.model.query
        latest_engineer_history = fil.order_by(self.model.payment_start_day.desc()).filter(
            self.model.engineer_id == engineer_id).first()
        if latest_engineer_history is None:
            latest_engineer_history = self.create()
        return latest_engineer_history

    def find_all_order_by_start_day(self):
        return self.model.query.order_by(self.model.engineer_id.asc(), self.model.payment_start_day.desc()).all()

    def get_history_by_date(self, engineer_id, date):
        fil = self.model.query
        engineer_history_at_date = fil.filter(self.model.engineer_id == engineer_id,
                                              self.model.payment_start_day <= date,
                                              date <= self.model.payment_end_day).first()
        return engineer_history_at_date

    def get_history_at_result_month(self, engineer_id, month):
        fil = self.model.query
        engineer_history = fil.filter(self.model.engineer_id == engineer_id,
                                      self.model.payment_start_day <= month, month <= self.model.payment_end_day
                                      ).first()
        return engineer_history

    def create(self):
        return EngineerHistory()
