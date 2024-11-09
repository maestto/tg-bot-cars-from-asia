from sqlalchemy import Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from tgbot.models.db.base import Base


class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
