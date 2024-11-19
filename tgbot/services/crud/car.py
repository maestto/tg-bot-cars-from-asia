from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from models.db.car import Car


class CarCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_car(self, brand: str, model: str, year: int, price: float, photo_file_id: str):
        new_car = Car(brand=brand, model=model, year=year, price=price, photo_file_id=photo_file_id)
        self.db.add(new_car)
        await self.db.commit()
        await self.db.refresh(new_car)
        return new_car

    async def get_cars(self, offset: int = 0, limit: int = 5):
        query = select(Car).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_cars_paginated(self, page: int, items_per_page: int):
        offset = (page - 1) * items_per_page
        query = select(Car).offset(offset).limit(items_per_page)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_car_by_id(self, car_id: int):
        query = select(Car).where(Car.id == car_id)
        result = await self.db.execute(query)
        return result.scalar()

    async def filter_cars(self, filters: dict):
        query = select(Car)
        for key, value in filters.items():
            if not value or str(value).lower() == "пусто":
                continue
            column = getattr(Car, key, None)
            if isinstance(column, InstrumentedAttribute):
                query = query.where(column == value)
        result = await self.db.execute(query)
        return result.scalars().all()



