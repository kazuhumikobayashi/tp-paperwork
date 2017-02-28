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

    def __repr__(self):
        pass
