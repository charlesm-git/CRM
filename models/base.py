from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select


class Base(DeclarativeBase):
    @classmethod
    def get_all(cls, session):
        return session.scalars(select(cls)).all()

    @classmethod
    def get_by_id(cls, session, id):
        return session.get(cls, id)

    @classmethod
    def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            if value != "":
                setattr(self, key, value)
        session.commit()
        session.refresh(self)

    def delete(self, session):
        session.delete(self)
        session.commit()
