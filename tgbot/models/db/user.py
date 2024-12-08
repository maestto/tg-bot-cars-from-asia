from datetime import datetime

from sqlalchemy import Integer, BigInteger, String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from tgbot.models.db.base import Base


class User(Base):
    __tablename__ = "User"
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(13), nullable=False)
    datetime_of_registration: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
