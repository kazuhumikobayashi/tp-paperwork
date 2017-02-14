from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.company import Company
from application.domain.model.engineer_skill import EngineerSkill


class Engineer(BaseModel, db.Model):
    __tablename__ = 'engineers'
    PER_PAGE = 10

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    engineer_name = Column(String(128))
    engineer_name_kana = Column(String(128))
    company_id = Column(Integer, ForeignKey("companies.id"))
    remarks = Column(String(1024))

    company = relationship(Company, lazy='joined')
    engineer_skills = relationship(EngineerSkill, cascade='all, delete-orphan')

    def __init__(self,
                 start_date=None,
                 end_date=None,
                 engineer_name=None,
                 engineer_name_kana=None,
                 company_id=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Engineer, self).__init__(created_at, created_user, updated_at, updated_user)
        self.start_date = start_date
        self.end_date = end_date
        self.engineer_name = engineer_name
        self.engineer_name_kana = engineer_name_kana
        self.company_id = company_id
        self.remarks = remarks

    def __repr__(self):
        return "<Engineer:" + \
                "'id='{}".format(self.id) + \
                "', start_date='{}".format(self.start_date) + \
                "', end_date='{}".format(self.end_date) + \
                "', engineer_name='{}".format(self.engineer_name) + \
                "', engineer_name_kana='{}".format(self.engineer_name_kana) + \
                "', company_id='{}".format(self.company_id) + \
                "', remarks='{}".format(self.remarks) + \
                "', engineer_skills='{}".format(self.engineer_skills) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
