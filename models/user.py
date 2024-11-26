from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, DateTime, select

from models.database import Base
import models.role
import models.client
import models.event


class User(Base):
    __tablename__ = "crm_user"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(320))
    password: Mapped[str] = mapped_column(String(255))
    date_created: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )
    date_updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="RESTRICT", onupdate="CASCADE")
    )

    # Relationship
    role: Mapped["models.role.Role"] = relationship(
        "Role", back_populates="users"
    )
    clients: Mapped[Optional[List["models.client.Client"]]] = relationship(
        "Client", back_populates="sales_contact"
    )
    events: Mapped[Optional[List["models.event.Event"]]] = relationship(
        "Event", back_populates="support_contact"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

    def has_permission(self, action):
        role_permission = {
            "sales": [
                "create-client",
                "update-client",
                "delete-client",
                "update-contract",
                "create-event",
                "update-event",
            ],
            "management": [
                "create-user",
                "update-user",
                "delete-user",
                "create-contract",
                "update-contract",
                "assign-support-contact-to-event",
            ],
            "support": ["update-event"],
        }
        return action in role_permission.get(self.role.name, [])

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    @classmethod
    def get_all_users(cls, session):
        return session.scalar(select(cls))

    @classmethod
    def get_by_id(cls, session, id):
        return session.get(cls, id)
