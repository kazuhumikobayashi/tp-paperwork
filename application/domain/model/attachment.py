from sqlalchemy import Column, Integer, String

from application import db
from application.domain.model.base_model import BaseModel


class Attachment(BaseModel, db.Model):
    __tablename__ = 'attachments'
    PER_PAGE = 10

    filename = Column(String(256), nullable=False)
    storage_filename = Column(String(256), nullable=False)
    size = Column(Integer, nullable=False)
    content_type = Column(String(256))

    def __init__(self,
                 filename=None,
                 storage_filename=None,
                 size=None,
                 content_type=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Attachment, self).__init__(created_at, created_user, updated_at, updated_user)
        self.filename = filename
        self.storage_filename = storage_filename
        self.size = size
        self.content_type = content_type

    def __repr__(self):
        return "<Attachment:" + \
                "'id='{}".format(self.id) + \
                "', filename='{}".format(self.filename) + \
                "', storage_filename='{}".format(self.storage_filename) + \
                "', size='{}".format(self.size) + \
                "', content_type='{}".format(self.content_type) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
