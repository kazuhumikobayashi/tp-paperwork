from application.domain.repository.destination_repository import DestinationRepository


class DestinationService(object):
    repository = DestinationRepository()

    def find(self, page, company_id, destination_name, destination_department):
        return self.repository.find(page, company_id, destination_name, destination_department)

    def find_by_id(self, user_id):
        return self.repository.find_by_id(user_id)

    def save(self, user):
        return self.repository.save(user)

    def destroy(self, user):
        return self.repository.destroy(user)
