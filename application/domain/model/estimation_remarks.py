from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey

from application import db
from application.domain.model.base_model import BaseModel


class EstimationRemarks(BaseModel, db.Model):
    __tablename__ = 'estimation_remarks'
    PER_PAGE = 10

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    scope = Column(String(1024))
    contents = Column(String(1024))
    deliverables = Column(String(1024))
    delivery_place = Column(String(1024))
    inspection_date = Column(Date)
    responsible_person = Column(String(128))
    quality_control = Column(String(128))
    subcontractor = Column(String(128))

    def __init__(self,
                 project_id=None,
                 scope=None,
                 contents=None,
                 deliverables=None,
                 delivery_place=None,
                 inspection_date=None,
                 responsible_person=None,
                 quality_control=None,
                 subcontractor=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(EstimationRemarks, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.scope = scope
        self.contents = contents
        self.deliverables = deliverables
        self.delivery_place = delivery_place
        self.inspection_date = inspection_date
        self.responsible_person = responsible_person
        self.quality_control = quality_control
        self.subcontractor = subcontractor

    def __repr__(self):
        return "<EstimationRemarks:" + \
                "'id='{}".format(self.id) + \
                "', project_id='{}".format(self.project_id) + \
                "', scope='{}".format(self.scope) + \
                "', contents='{}".format(self.contents) + \
                "', deliverables='{}".format(self.deliverables) + \
                "', delivery_place='{}".format(self.delivery_place) + \
                "', inspection_date='{}".format(self.inspection_date) + \
                "', responsible_person='{}".format(self.responsible_person) + \
                "', quality_control='{}".format(self.quality_control) + \
                "', subcontractor='{}".format(self.subcontractor) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

    def clone(self):
        arguments = dict()
        copy = EstimationRemarks()
        for name, column in self.__mapper__.columns.items():
            if not (column.primary_key or column.unique):
                arguments[name] = getattr(self, name)
        return copy.__class__(**arguments)
