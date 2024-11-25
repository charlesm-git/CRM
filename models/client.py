from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, DateTime


from models.database import Base
import models.contract
import models.user


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(320), unique=True)
    phone_number: Mapped[str] = mapped_column(String(20))
    company: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    date_created: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )
    date_updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    sales_contact_id: Mapped[int] = mapped_column(
        ForeignKey("crm_user.id", ondelete="RESTRICT", onupdate="CASCADE")
    )

    # Relationship
    contracts: Mapped[Optional[List["models.contract.Contract"]]] = relationship(
        back_populates="client"
    )
    sales_contact: Mapped["models.user.User"] = relationship(back_populates="clients")

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}')>"
