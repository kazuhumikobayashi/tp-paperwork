from application.domain.model.company import Company
from application.domain.repository.base_repository import BaseRepository


class CompanyRepository(BaseRepository):

    model = Company

    def find(self, page, company_name, company_code):
        fil = self.model.query
        if company_name:
            fil = fil.filter(self.model.company_name.like('%' + company_name + '%'))
        if company_code:
            fil = fil.filter(self.model.company_code.like('%' + company_code + '%'))
        pagination = fil.paginate(page, self.model.PER_PAGE)
        return pagination

    def create(self):
        return Company()
