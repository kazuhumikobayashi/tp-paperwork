from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel


class Destination(BaseModel, db.Model):
    __tablename__ = 'destinations'
    PER_PAGE = 10

    company_id = Column(Integer, ForeignKey("companies.id"))
    destination_name = Column(String(128), nullable=False)
    destination_department = Column(String(128))

    company = relationship("Company", lazy='joined')

    def __init__(self,
                 company_id=None,
                 destination_name=None,
                 destination_department=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Destination, self).__init__(created_at, created_user, updated_at, updated_user)
        self.company_id = company_id
        self.destination_name = destination_name
        self.destination_department = destination_department

    def __repr__(self):
        return "<Destination:" + \
                "'id='{}".format(self.id) + \
                "', company_id='{}".format(self.company_id) + \
                "', destination_name='{}".format(self.destination_name) + \
                "', destination_department='{}".format(self.destination_department) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
