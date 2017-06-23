from sqlalchemy import Column, Integer

from application import db
from application.domain.model.base_model import BaseModel


class OrderSequence(BaseModel, db.Model):
    __tablename__ = 'order_sequence'
    PER_PAGE = 10

    fiscal_year = Column(Integer, nullable=False)
    sequence = Column(Integer, nullable=False)

    def __init__(self,
                 fiscal_year=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(OrderSequence, self).__init__(created_at, created_user, updated_at, updated_user)
        self.fiscal_year = fiscal_year
        self.sequence = 1

    def get_bp_order_no(self):
        return 'C' + str(self.fiscal_year) + '-' + '{0:03d}'.format(self.sequence)

    def __repr__(self):
        return "<OrderSequence:" + \
                "'id='{}".format(self.id) + \
                "', fiscal_year='{}".format(self.fiscal_year) + \
                "', sequence='{}".format(self.sequence) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
