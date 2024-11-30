from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from tgbot.models.db.base import Base


class Car(Base):
    __tablename__ = "Cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    photo_file_id: Mapped[str] = mapped_column(String(255), nullable=False)
