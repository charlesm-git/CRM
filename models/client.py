from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, DateTime

from models.contract import Contract
from models.user import User
from models.database import Base


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(320))
    phone_number: Mapped[str] = mapped_column(String(20))
    company: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    date_created: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )
    date_updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    sales_contact_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Relationship
    contracts: Mapped[Optional[List["Contract"]]] = relationship(
        back_populates="client"
    )
    sales_contact: Mapped["User"] = relationship(back_populates="clients")

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}')>"
