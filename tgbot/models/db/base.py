from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_pool(pg_dsn: str, echo: bool) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(pg_dsn, echo=echo)
    async_session_local = async_sessionmaker(bind=engine,
                                             autocommit=False,
                                             autoflush=False,
                                             expire_on_commit=False,
                                             )
    return async_session_local
