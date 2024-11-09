from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from models.db.user import User as UserModel


class User:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def user_exists(self, user_tg_id: int) -> bool:
        """ Проверяет наличие пользователя в базе данных.  """
        query = exists(1).select_from(UserModel).where(UserModel.tg_id == user_tg_id).select()
        curr = await self.db.execute(query)
        return curr.scalar_one()

    async def insert_user(self, user_tg_id: int):
        user = UserModel(tg_id=user_tg_id)
        self.db.add(user)
        return

    async def get_user(self, user_tg_id: int) -> UserModel:
        query = select(UserModel).filter(UserModel.tg_id == user_tg_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def commit(self):
        await self.db.commit()
        return

    async def refresh(self, instance: object):
        await self.db.refresh(instance)
        return
