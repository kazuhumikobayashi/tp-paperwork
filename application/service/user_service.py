from application.domain.repository.user_repository import UserRepository


class UserService(object):
    repository = UserRepository()

    def find(self, page, user_name, shain_number):
        return self.repository.find(page, user_name, shain_number)

    def find_all(self, page):
        return self.repository.find_all(page)

    def find_by_id(self, user_id):
        return self.repository.find_by_id(user_id)

    def find_by_shain_number(self, shain_number):
        return self.repository.find_by_shain_number(shain_number)

    def save(self, user):
        return self.repository.save(user)

    def destroy(self, user):
        return self.repository.destroy(user)
