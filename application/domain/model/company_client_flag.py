from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.client_flag import ClientFlag


class CompanyClientFlag(BaseModel, db.Model):
    __tablename__ = 'company_client_flags'
    PER_PAGE = 10

    company_id = Column(Integer, ForeignKey("companies.id"))
    client_flag_id = Column(Integer, ForeignKey("client_flags.id"))

    client_flag = relationship(ClientFlag, lazy='joined')

    def __init__(self,
                 company_id=None,
                 client_flug_id=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(CompanyClientFlag, self).__init__(created_at, created_user, updated_at, updated_user)
        self.company_id = company_id
        self.client_flag_id = client_flug_id

    def __repr__(self):
        return "<CompanyClientFlag:" + \
                "'id='{}".format(self.id) + \
                "', company_id='{}".format(self.company_id) + \
                "', client_flag_id='{}".format(self.client_flag_id) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
