from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, DateTime, Text

from models.contract import Contract
from models.user import User
from models.database import Base


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contract.id", ondelete="CASCADE")
    )
    date_start: Mapped[datetime] = mapped_column(DateTime)
    date_end: Mapped[datetime] = mapped_column(DateTime)
    location: Mapped[str] = mapped_column(String(128))
    attendees: Mapped[int] = mapped_column(int)
    note: Mapped[Optional[str]] = mapped_column(Text)
    support_contact_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )

    # Relationship
    contract: Mapped["Contract"] = relationship(back_populates="event")
    support_contact: Mapped["User"] = relationship(back_populates="events")

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.contract_id}')>"
