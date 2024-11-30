from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, DateTime, select

from models.base import Base
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
        return f"{self.name} {self.surname} as {self.role.name}"

    @classmethod
    def get_user_from_email(cls, session, email):
        return session.scalar(select(cls).where(cls.email == email))