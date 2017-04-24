from application.domain.repository.client_flag_repository import ClientFlagRepository


class ClientFlagService(object):
    repository = ClientFlagRepository()

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_all_for_multi_select(self):
        client_flag_list = [(h.id, h.client_flag_name) for h in self.find_all()]
        return client_flag_list
