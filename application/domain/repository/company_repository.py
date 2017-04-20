from datetime import datetime

from flask import current_app
from flask import session

from application import db
from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.repository.base_repository import BaseRepository


class CompanyRepository(BaseRepository):

    model = Company

    def find(self, page, input_company_name, client_flag_id=None, bank_id=None):
        fil = self.model.query
        if input_company_name:
            fil = fil.filter(self.model.company_name.like('%' + input_company_name + '%') |
                              self.model.company_name_kana.like('%' + input_company_name + '%') |
                              self.model.company_name_abbreviated.like('%' + input_company_name + '%'))
        if client_flag_id and client_flag_id != '' and client_flag_id != [''] and client_flag_id != []:
            fil = fil.filter(self.model.company_client_flags.any(CompanyClientFlag.client_flag_id.in_(client_flag_id)))
        if bank_id and bank_id != '' and bank_id != [''] and bank_id != []:
            fil = fil.filter(self.model.bank_id.in_(bank_id))
        pagination = fil.order_by(self.model.company_name.asc()).paginate(page, self.model.PER_PAGE)
        return pagination

    def save(self, company):
        if company.id is None:
            company.created_at = datetime.today()
            company.created_user = session['user']['user_name']
        company.updated_at = datetime.today()
        company.updated_user = session['user']['user_name']
        for company_client_flugs in company.company_client_flags:
            company_client_flugs.created_at = datetime.today()
            company_client_flugs.created_user = session['user']['user_name']
            company_client_flugs.updated_at = datetime.today()
            company_client_flugs.updated_user = session['user']['user_name']

        db.session.add(company)
        db.session.commit()
        current_app.logger.debug('save:' + str(company))


    def create(self):
        return Company()
