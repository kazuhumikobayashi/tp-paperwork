from sqlalchemy import Column, String

from application import db
from application.domain.model.base_model import BaseModel


class ClientFlag(BaseModel, db.Model):
    __tablename__ = 'client_flags'
    PER_PAGE = 10

    client_flag_name = Column(String(32), nullable=False, unique=True)

    def __init__(self,
                 client_flag_name=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(ClientFlag, self).__init__(created_at, created_user, updated_at, updated_user)
        self.client_flag_name = client_flag_name

    def __repr__(self):
        return "<ClientFlug:" + \
                "'id='{}".format(self.id) + \
                "', client_flag_name='{}".format(self.client_flag_name) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
