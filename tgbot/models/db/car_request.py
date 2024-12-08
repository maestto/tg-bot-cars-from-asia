from datetime import datetime

from sqlalchemy import BigInteger, String, func, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from tgbot.models.db.base import Base


class CarRequest(Base):
    __tablename__ = "CarRequest"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("User.tg_id"), nullable=False)
    car_info: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[str] = mapped_column(String, nullable=False)
    additional_details: Mapped[str] = mapped_column(String, nullable=False)
    datetime_of_request: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
