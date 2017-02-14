from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.attachment import Attachment
from application.domain.model.base_model import BaseModel


class ProjectAttachment(BaseModel, db.Model):
    __tablename__ = 'project_attachments'
    PER_PAGE = 10

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    attachment_id = Column(Integer, ForeignKey("attachments.id"), nullable=False)
    type = Column(String(1), nullable=False)
    remarks = Column(String(256))

    attachment = relationship(Attachment, lazy='subquery')

    def __init__(self,
                 project_id=None,
                 attachment_id=None,
                 type=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(ProjectAttachment, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.attachment_id = attachment_id
        self.type = type
        self.remarks = remarks

    def __repr__(self):
        return "<ProjectAttachment:" + \
                "'id='{}".format(self.id) + \
                "', project_id='{}".format(self.project_id) + \
                "', attachment_id='{}".format(self.attachment_id) + \
                "', type='{}".format(self.type) + \
                "', remarks='{}".format(self.remarks) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"
