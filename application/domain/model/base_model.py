from sqlalchemy import Column, Integer, String, DateTime


class BaseModel(object):
    __tablename__ = None
    PER_PAGE = 10

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False)
    created_user = Column(String(128), nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_user = Column(String(128), nullable=False)

    def __init__(self,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        self.created_at = created_at
        self.created_user = created_user
        self.updated_at = updated_at
        self.updated_user = updated_user

    def clone(self):
        arguments = dict()
        copy = type(self)()
        for name, column in self.__mapper__.columns.items():
            if name[0:1] == '_':
                name = name[1:]
            if not (column.primary_key or column.unique):
                arguments[name] = getattr(self, name)
        return copy.__class__(**arguments)

    def __repr__(self):
        pass
