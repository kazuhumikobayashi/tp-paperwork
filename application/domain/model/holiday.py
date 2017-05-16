from sqlalchemy import Column, String, Date

from application import db
from application.domain.model.base_model import BaseModel


class Holiday(BaseModel, db.Model):
    __tablename__ = 'holidays'

    holiday = Column(Date, nullable=False)
    holiday_name = Column(String(128))

    def __init__(self,
                 holiday=None,
                 holiday_name=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Holiday, self).__init__(created_at, created_user, updated_at, updated_user)
        self.holiday = holiday
        self.holiday_name = holiday_name

    def __repr__(self):
        return "<Holiday:" + \
                "'id='{}".format(self.id) + \
                "', holiday='{}".format(self.holiday) + \
                "', holiday_name='{}".format(self.holiday_name) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
