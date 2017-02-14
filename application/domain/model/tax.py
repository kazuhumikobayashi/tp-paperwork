from sqlalchemy import Column, Date, DECIMAL

from application import db
from application.domain.model.base_model import BaseModel


class Tax(BaseModel, db.Model):
    __tablename__ = 'tax'
    PER_PAGE = 10

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    tax_rate = Column(DECIMAL(6,2))

    def __init__(self,
                 start_date=None,
                 end_date=None,
                 tax_rate=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Tax, self).__init__(created_at, created_user, updated_at, updated_user)
        self.start_date = start_date
        self.end_date = end_date
        self.tax_rate = tax_rate

    def __repr__(self):
        return "<Tax:" + \
                "'id='{}".format(self.id) + \
                "', start_date='{}".format(self.start_date) + \
                "', end_date='{}".format(self.end_date) + \
                "', tax_rate='{}".format(self.tax_rate) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
