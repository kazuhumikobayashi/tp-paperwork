import itertools

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
        latest_history_list = []
        for key, items in group_bys:
            lists = list(items)
            item = lists[0]
            if len(lists) > 1:
                # 契約開始日付の降順でsortしているので、最後のデータの契約開始日付に上書き
                item.payment_start_day = lists[len(lists)-1].payment_start_day
            latest_history_list.append(item)

        ret = [('', '', '', '')]
        engineer_list = \
            [(str(h.engineer_id),
              h.engineer.engineer_name + '【契約終了】' if h.is_contract() else h.engineer.engineer_name,
              h.is_contract(),
              '契約期間：{} - {}'.format(h.payment_start_day.strftime('%Y/%m/%d'),
                                    h.payment_end_day.strftime('%Y/%m/%d')))
             for h in latest_history_list]
        ret.extend(engineer_list)
        return ret
