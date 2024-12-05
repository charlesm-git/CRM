from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from models.base import Base
import models.user


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(16))

    # Relationship
    users: Mapped[Optional[List["models.user.User"]]] = relationship(
        back_populates="role"
    )

    def __repr__(self):
        return f"{self.name}"
