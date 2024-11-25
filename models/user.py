from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, DateTime

from models.role import Role
from models.database import Base
from models.client import Client
from models.event import Event


class User(Base):
    __tablename__ = "users"

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
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    # Relationship
    role: Mapped["Role"] = relationship(back_populates="users")
    clients: Mapped[Optional[List["Client"]]] = relationship(
        back_populates="sales_contact"
    )
    events: Mapped[Optional[List["Event"]]] = relationship(
        back_populates="support_contact"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"
