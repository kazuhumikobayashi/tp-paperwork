from application.domain.repository.business_category_repository import BusinessCategoryRepository


class BusinessCategoryService(object):
    repository = BusinessCategoryRepository()

    def find(self, page, business_category_name):
        return self.repository.find(page, business_category_name)

    def find_all(self, page=None):
        return self.repository.find_all(page)
 
    def find_all_for_multi_select(self):
        business_category_list = [(h.id, h.business_category_name) for h in self.find_all()]
        return business_category_list

    def find_by_id(self, business_category_id):
        return self.repository.find_by_id(business_category_id)

    def save(self, business_category):
        return self.repository.save(business_category)

    def destroy(self, business_category):
        return self.repository.destroy(business_category)
