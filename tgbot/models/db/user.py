from sqlalchemy import Integer, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from tgbot.models.db.base import Base


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(13), nullable=False)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
