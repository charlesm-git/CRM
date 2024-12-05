from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Boolean, ForeignKey, Integer, DateTime

from models.base import Base
import models.client
import models.event

class Contract(Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client.id", ondelete="CASCADE")
    )

    # Relationship
    client: Mapped["models.client.Client"] = relationship(back_populates="contracts")
    event: Mapped["models.event.Event"] = relationship(back_populates="contract")

    def __repr__(self):
        return f"Contract n°{self.id}"
    
    def __str__(self):
        return f"Contract n°{self.id}"
