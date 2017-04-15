from datetime import datetime

from flask import current_app
from flask import session

from application import db
from application.domain.model.company import Company
from application.domain.model.engineer import Engineer
from application.domain.model.engineer_skill import EngineerSkill
from application.domain.model.engineer_business_category import EngineerBusinessCategory
from application.domain.repository.base_repository import BaseRepository


class EngineerRepository(BaseRepository):

    model = Engineer

    def find(self, page, engineer_name, company_id, skill_id=None, business_category_id=None):
        query = self.model.query
        if engineer_name:
            query = query.filter(self.model.engineer_name.like('%' + engineer_name + '%'))
        if company_id and company_id != '' and company_id != [''] and company_id != []:
            query = query.filter(self.model.company_id.in_(company_id))
        if skill_id and skill_id != '' and skill_id != [''] and skill_id != []:
            query = query.filter(self.model.engineer_skills.any(EngineerSkill.skill_id.in_(skill_id)))
        if business_category_id and business_category_id != '' and business_category_id != [''] and business_category_id != []:
            query = query.filter(self.model.engineer_business_categories.any(EngineerBusinessCategory.business_category_id.in_(business_category_id)))
        pagination = \
            query.join(Company, Engineer.company)\
            .order_by(Company.company_name.asc(), self.model.engineer_name_kana.asc())\
            .paginate(page, self.model.PER_PAGE)
        return pagination

    def save(self, engineer):
        if engineer.id is None:
            engineer.created_at = datetime.today()
            engineer.created_user = session['user']['user_name']
        engineer.updated_at = datetime.today()
        engineer.updated_user = session['user']['user_name']
        for engineer_skills in engineer.engineer_skills:
            engineer_skills.created_at = datetime.today()
            engineer_skills.created_user = session['user']['user_name']
            engineer_skills.updated_at = datetime.today()
            engineer_skills.updated_user = session['user']['user_name']
        for engineer_business_categories in engineer.engineer_business_categories:
            engineer_business_categories.created_at = datetime.today()
            engineer_business_categories.created_user = session['user']['user_name']
            engineer_business_categories.updated_at = datetime.today()
            engineer_business_categories.updated_user = session['user']['user_name']

        db.session.add(engineer)
        db.session.commit()
        current_app.logger.debug('save:' + str(engineer))

    def create(self):
        return Engineer()
