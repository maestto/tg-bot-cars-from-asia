from aiogram import Dispatcher, Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.common import command_start
from states.car import CarForm
from services.crud.car import CarCRUD


async def start_add_car(msg: Message, state: FSMContext):
    await msg.answer("Введите марку автомобиля:")
    await state.set_state(CarForm.brand)


async def process_brand(msg: Message, state: FSMContext):
    await state.update_data(brand=msg.text)
    await msg.answer("Введите модель автомобиля:")
    await state.set_state(CarForm.model)


async def process_model(msg: Message, state: FSMContext):
    await state.update_data(model=msg.text)
    await msg.answer("Введите год выпуска автомобиля:")
    await state.set_state(CarForm.year)


async def process_year(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer("Пожалуйста, введите числовое значение года.")
        return
    await state.update_data(year=int(msg.text))
    await msg.answer("Введите цену автомобиля:")
    await state.set_state(CarForm.price)


async def process_price(msg: Message, state: FSMContext):
    try:
        price = float(msg.text)
        await state.update_data(price=price)
        await msg.answer("Отправьте фотографию автомобиля:")
        await state.set_state(CarForm.photo)
    except ValueError:
        await msg.answer("Пожалуйста, введите корректное числовое значение для цены.")


async def process_photo(msg: Message, state: FSMContext, db: AsyncSession):
    if not msg.photo:
        await msg.answer("Пожалуйста, отправьте фотографию автомобиля.")
        return

    photo_file_id = msg.photo[-1].file_id
    await state.update_data(photo_file_id=photo_file_id)

    data = await state.get_data()
    car_crud = CarCRUD(db)
    await car_crud.add_car(
        brand=data['brand'],
        model=data['model'],
        year=data['year'],
        price=data['price'],
        photo_file_id=data['photo_file_id']
    )

    await msg.answer("Машина успешно добавлена в базу данных!")
    await command_start(msg, db, state)


async def cancel(msg: Message, state: FSMContext, db: AsyncSession):
    await state.clear()
    await msg.answer("Отменено")
    await command_start(msg, db, state)


def register_handlers_add_car(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(cancel, Command("cancel")) #AdminFilter()

    router.message.register(start_add_car, lambda msg: msg.text == "Добавить машину")
    router.message.register(process_brand, CarForm.brand)
    router.message.register(process_model, CarForm.model)
    router.message.register(process_year, CarForm.year)
    router.message.register(process_price, CarForm.price)
    router.message.register(process_photo, CarForm.photo, F.photo)
    dp.include_router(router)
