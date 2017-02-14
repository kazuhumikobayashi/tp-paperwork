from sqlalchemy import Column
from sqlalchemy import String

from application import db
from application.domain.model.base_model import BaseModel


class ContractForm(BaseModel, db.Model):
    __tablename__ = 'contract_forms'
    PER_PAGE = 10

    contract_form_name = Column(String(32), nullable=False)

    def __init__(self,
                 contract_form_name=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(ContractForm, self).__init__(created_at, created_user, updated_at, updated_user)
        self.contract_form_name = contract_form_name

    def __repr__(self):
        return "<ContractForm:" + \
                "'id='{}".format(self.id) + \
                "', contract_form_name='{}".format(self.contract_form_name) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
