from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, DateTime, Text

from models.base import Base
import models.user
import models.contract

class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(128))
    attendees: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    note: Mapped[Optional[str]] = mapped_column(Text)
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contract.id", ondelete="CASCADE")
    )
    support_contact_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("crm_user.id", ondelete="SET NULL")
    )

    # Relationship
    contract: Mapped["models.contract.Contract"] = relationship(back_populates="event")
    support_contact: Mapped["models.user.User"] = relationship(back_populates="events")

    def __repr__(self):
        return f"Event n°{self.id}"
