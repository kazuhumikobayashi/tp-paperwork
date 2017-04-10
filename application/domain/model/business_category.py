from sqlalchemy import Column, String

from application import db
from application.domain.model.base_model import BaseModel


class BusinessCategory(BaseModel, db.Model):
    __tablename__ = 'business_categories'
    PER_PAGE = 10

    business_category_name = Column(String(32), nullable=False, unique=True)

    def __init__(self,
                 business_category_name=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(BusinessCategory, self).__init__(created_at, created_user, updated_at, updated_user)
        self.business_category_name = business_category_name

    def __repr__(self):
        return "<BusinessCategory:" + \
                "'id='{}".format(self.id) + \
                "', business_category_name='{}".format(self.business_category_name) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
