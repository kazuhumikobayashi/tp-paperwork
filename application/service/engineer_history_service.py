import itertools

from flask import current_app

from application.domain.repository.engineer_history_repository import EngineerHistoryRepository


class EngineerHistoryService(object):
    repository = EngineerHistoryRepository()

    def find_by_id(self, engineer_history_id):
        return self.repository.find_by_id(engineer_history_id)

    def find_by_engineer_id(self, engineer_id):
        return self.repository.find_by_engineer_id(engineer_id)

    def get_latest_history(self, engineer_id):
        return self.repository.get_latest_history(engineer_id)

    def get_history_by_start_day(self, engineer_id, billing_start_day):
        return self.repository.get_history_by_date(engineer_id, billing_start_day)

    def get_history_at_result_month(self, engineer_id, month):
        return self.repository.get_history_at_result_month(engineer_id, month)

    def save(self, engineer_history):
        return self.repository.save(engineer_history)

    def destroy(self, engineer_history):
        return self.repository.destroy(engineer_history)

    def find_contract_for_select(self):
        all_list = self.repository.find_all_order_by_start_day()
        group_bys = itertools.groupby(all_list, key=lambda x: x.engineer_id)
        # 契約開始日付の降順でsortしているので、1件目のデータのみリストに追加
        latest_history_list = [list(items)[0] for key, items in group_bys]

        ret = [('', '', '')]
        engineer_list = \
            [(str(h.engineer_id),
              h.engineer.engineer_name + '【契約終了】' if h.is_contract() else h.engineer.engineer_name,
              h.is_contract()) for h in latest_history_list]
        ret.extend(engineer_list)
        return ret
