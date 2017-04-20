from application.domain.repository.client_flag_repository import ClientFlagRepository


class ClientFlagService(object):
    repository = ClientFlagRepository()

    def find(self, page, client_flag_name):
        return self.repository.find(page, client_flag_name)

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_all_for_multi_select(self):
        client_flag_list = [(h.id, h.client_flag_name) for h in self.find_all()]
        return client_flag_list

    def find_by_id(self, client_flag_id):
        return self.repository.find_by_id(client_flag_id)

    def save(self, client_flug):
        return self.repository.save(client_flug)

    def destroy(self, client_flug):
        return self.repository.destroy(client_flug)
