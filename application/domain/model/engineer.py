from datetime import datetime

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.company import Company
from application.domain.model.engineer_business_category import EngineerBusinessCategory
from application.domain.model.engineer_history import EngineerHistory
from application.domain.model.engineer_skill import EngineerSkill
from application.domain.model.project_detail import ProjectDetail
from application.domain.model.immutables.gender import Gender
from application.domain.model.sqlalchemy.types import EnumType


class Engineer(BaseModel, db.Model):
    __tablename__ = 'engineers'
    PER_PAGE = 10

    engineer_name = Column(String(128), nullable=False)
    engineer_name_kana = Column(String(128))
    birthday = Column(Date)
    gender = Column(EnumType(enum_class=Gender))
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship(Company, lazy='joined')
    engineer_skills = relationship(EngineerSkill, cascade='all, delete-orphan')
    engineer_business_categories = relationship(EngineerBusinessCategory, cascade='all, delete-orphan')
    engineer_histories = relationship(EngineerHistory, cascade='all, delete-orphan')
    project_details = relationship(ProjectDetail, cascade='all, delete-orphan')

    def __init__(self,
                 engineer_name=None,
                 engineer_name_kana=None,
                 birthday=None,
                 gender=None,
                 company_id=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Engineer, self).__init__(created_at, created_user, updated_at, updated_user)
        self.engineer_name = engineer_name
        self.engineer_name_kana = engineer_name_kana
        self.birthday = birthday
        self.gender = gender
        self.company_id = company_id

    def is_bp(self):
        return self.company and self.company.is_bp()

    # 指定された日の期間内にある支払いサイトを返却
    def get_payment_site_by_date(self, date):
        for history in self.engineer_histories:
            if history.payment_start_day <= date <= history.payment_end_day:
                return history.payment_site
        return None

    # 指定された日の期間内にある履歴を返却
    def get_histories_by_date(self, date):
        for h in self.engineer_histories:
            if h.payment_start_day <= date <= h.payment_end_day:
                return h
        return EngineerHistory()

    def get_age(self):

        age = ""
        if self.birthday:
            today = int(datetime.today().date().strftime('%Y%m%d'))
            birthday = int(self.birthday.strftime('%Y%m%d'))
            age = int((today - birthday) / 10000)
        return age

    def __repr__(self):
        return "<Engineer:" + \
                "'id='{}".format(self.id) + \
                "', engineer_name='{}".format(self.engineer_name) + \
                "', engineer_name_kana='{}".format(self.engineer_name_kana) + \
                "', birthday='{}".format(self.birthday) + \
                "', gender='{}".format(self.gender) + \
                "', company='{}".format(self.company) + \
                "', engineer_skills='{}".format(self.engineer_skills) + \
                "', engineer_business_categories='{}".format(self.engineer_business_categories) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
