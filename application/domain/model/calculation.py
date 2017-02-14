from sqlalchemy import Column, String, Integer

from application import db
from application.domain.model.base_model import BaseModel


class Calculation(BaseModel, db.Model):
    __tablename__ = 'calculations'
    PER_PAGE = 10

    calculation_name = Column(String(32), nullable=False)
    amount = Column(Integer, nullable=False)
    formula = Column(Integer, nullable=False)

    def __init__(self,
                 calculation_name=None,
                 amount=None,
                 formula=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Calculation, self).__init__(created_at, created_user, updated_at, updated_user)
        self.calculation_name = calculation_name
        self.amount = amount
        self.formula = formula

    def __repr__(self):
        return "<Calculation:" + \
                "'id='{}".format(self.id) + \
                "', calculation_name='{}".format(self.calculation_name) + \
                "', amount='{}".format(self.amount) + \
                "', formula='{}".format(self.formula) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
