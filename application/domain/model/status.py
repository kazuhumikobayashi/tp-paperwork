from sqlalchemy import Column, String

from application import db
from application.domain.model.base_model import BaseModel


class Status(BaseModel, db.Model):
    __tablename__ = 'statuses'
    PER_PAGE = 10

    status_name = Column(String(32), nullable=False)

    def __init__(self,
                 status_name=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Status, self).__init__(created_at, created_user, updated_at, updated_user)
        self.status_name = status_name

    def __repr__(self):
        return "<Status:" + \
                "'id='{}".format(self.id) + \
                "', status_name='{}".format(self.status_name) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
