from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Boolean, ForeignKey, Integer, DateTime

from models.client import Client
from models.event import Event
from models.database import Base


class Contract(Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client.id", ondelete="CASCADE")
    )
    total_contract_amount: Mapped[int] = mapped_column(Integer)
    remaining_amount_to_pay: Mapped[int] = mapped_column(Integer)
    date_created: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )
    date_updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    contract_signed_status: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    # Relationship
    client: Mapped["Client"] = relationship(back_populates="contracts")
    event: Mapped["Event"] = relationship(back_populates="contract")

    def __repr__(self):
        return f"<Contract(id={self.id}, client_id='{self.client_id}')>"
