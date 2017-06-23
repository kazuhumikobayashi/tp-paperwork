from sqlalchemy import Column, Integer

from application import db
from application.domain.model.base_model import BaseModel


class BillingSequence(BaseModel, db.Model):
    __tablename__ = 'billing_sequence'
    PER_PAGE = 10

    fiscal_year = Column(Integer, nullable=False)
    sequence = Column(Integer, nullable=False)

    def __init__(self,
                 fiscal_year=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(BillingSequence, self).__init__(created_at, created_user, updated_at, updated_user)
        self.fiscal_year = fiscal_year
        self.sequence = 1

    def get_client_billing_no(self):
        return 'B' + str(self.fiscal_year) + '-' + '{0:03d}'.format(self.sequence)

    def __repr__(self):
        return "<BillingSequence:" + \
                "'id='{}".format(self.id) + \
                "', fiscal_year='{}".format(self.fiscal_year) + \
                "', sequence='{}".format(self.sequence) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
