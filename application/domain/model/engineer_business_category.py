from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.business_category import BusinessCategory


class EngineerBusinessCategory(BaseModel, db.Model):
    __tablename__ = 'engineer_business_categories'
    PER_PAGE = 10

    engineer_id = Column(Integer, ForeignKey("engineers.id"))
    business_category_id = Column(Integer, ForeignKey("business_categories.id"))

    business_category = relationship(BusinessCategory, lazy='joined')

    def __init__(self,
                 engineer_id=None,
                 business_category_id=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(EngineerBusinessCategory, self).__init__(created_at, created_user, updated_at, updated_user)
        self.engineer_id = engineer_id
        self.business_category_id = business_category_id

    def __repr__(self):
        return "<EngineerSkill:" + \
                "'id='{}".format(self.id) + \
                "', engineer_id='{}".format(self.engineer_id) + \
                "', business_category_id='{}".format(self.business_category_id) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
