from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel


class Bank(BaseModel, db.Model):
    __tablename__ = 'banks'

    bank_name = Column(String(32))
    text_for_document = Column(String(128))
    companies = relationship("Company", foreign_keys="Company.bank_id")

    def __init__(self,
                 bank_name=None,
                 text_for_document=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Bank, self).__init__(created_at, created_user, updated_at, updated_user)
        self.bank_name = bank_name
        self.text_for_document = text_for_document

    # 銀行が他のmodelと紐づいているならtrue
    def has_relationship(self):
        return self.companies

    def __repr__(self):
        return "<Bank:" + \
                "'id='{}".format(self.id) + \
                "', bank_name='{}".format(self.bank_name) + \
                "', text_for_document='{}".format(self.text_for_document) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
