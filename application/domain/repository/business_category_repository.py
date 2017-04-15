from application.domain.model.business_category import BusinessCategory
from application.domain.repository.base_repository import BaseRepository


class BusinessCategoryRepository(BaseRepository):

    model = BusinessCategory

    def find(self, page, business_category_name):
        query = self.model.query
        if business_category_name:
            query = query.filter(self.model.business_category_name.like('%' + business_category_name + '%'))
        pagination = query.order_by(self.model.business_category_name.asc()).paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_name(self, business_category_name):
        return self.model.query.filter(self.model.business_category_name == business_category_name).first()

    def create(self):
        return BusinessCategory()
