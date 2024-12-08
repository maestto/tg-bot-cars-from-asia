from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.db.car_request import CarRequest as CarRequestModel


class CarRequest:

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_car_request(self, cr_id: int) -> CarRequestModel:
        query = select(CarRequestModel).filter(CarRequestModel.id == cr_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    def insert_car_request(self, tg_id: int, car_info: str, price: str, additional_details: str):
        user = CarRequestModel(tg_id=tg_id, car_info=car_info, price=price, additional_details=additional_details)
        self.db.add(user)
        return user

    async def commit(self):
        await self.db.commit()
        return

    async def refresh(self, instance: object):
        await self.db.refresh(instance)
        return
