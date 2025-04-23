from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    create_dt = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    modify_dt = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                       onupdate=lambda: datetime.now(timezone.utc))
    is_delete = Column(Boolean, default=False)

    def as_dict(self, **renames):
        if not renames:
            return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        else:
            return {renames.get(c.name, c.name): getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def _fetch(cls, session, **kwargs):
        return session.query(cls).filter_by(**kwargs).first()