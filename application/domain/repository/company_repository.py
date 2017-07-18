from datetime import datetime

from dateutil.tz import tz
from flask import current_app
from flask import session

from application import db
from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.repository.base_repository import BaseRepository


class CompanyRepository(BaseRepository):

    model = Company

    def find(self, page, company_name, client_flag=None, bank_id=None):
        fil = self.model.query
        if company_name:
            fil = fil.filter(self.model.company_name.like('%' + company_name + '%') |
                             self.model.company_name_kana.like('%' + company_name + '%') |
                             self.model.company_short_name.like('%' + company_name + '%'))
        if client_flag and client_flag != '' and client_flag != [''] and client_flag != []:
            flags = [ClientFlag.parse(flag) for flag in client_flag]
            fil = fil.filter(self.model.company_client_flags.any(CompanyClientFlag.client_flag.in_(flags)))
        if bank_id and bank_id != '' and bank_id != [''] and bank_id != []:
            fil = fil.filter(self.model.bank_id.in_(bank_id))
        pagination = fil.order_by(self.model.company_name.asc()).paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_client_flag(self, client_flag):
        fil = self.model.query
        flags = [ClientFlag.parse(flag) for flag in client_flag]
        companies = fil.filter(self.model.company_client_flags.any(
                               CompanyClientFlag.client_flag.in_(flags))).all()
        return companies

    def save(self, company):
        jst = tz.gettz('Asia/Tokyo')
        now = datetime.now(jst)
        if company.id is None:
            company.created_at = now
            company.created_user = session['user']['user_name']
        company.updated_at = now
        company.updated_user = session['user']['user_name']
        for company_client_flags in company.company_client_flags:
            company_client_flags.created_at = now
            company_client_flags.created_user = session['user']['user_name']
            company_client_flags.updated_at = now
            company_client_flags.updated_user = session['user']['user_name']

        db.session.add(company)
        db.session.commit()
        current_app.logger.debug('save:' + str(company))

    def create(self):
        return Company()
