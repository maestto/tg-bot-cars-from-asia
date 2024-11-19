from aiogram import Dispatcher, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from services.crud.car import CarCRUD


async def list_cars(msg: Message, db: AsyncSession, page: int = 1):
    items_per_page = 5
    car_crud = CarCRUD(db)

    cars_query = await car_crud.get_cars_paginated(page, items_per_page)

    kb = InlineKeyboardBuilder()

    for car in cars_query:
        text = f"{car.brand} {car.model} ({car.year}) - {car.price}₽"
        kb.add(
            InlineKeyboardButton(
                text=text,
                callback_data=f"car_{car.id}"
            )
        )

    next_page_cars = await car_crud.get_cars_paginated(page + 1, items_per_page)

    if next_page_cars:
        kb.add(
            InlineKeyboardButton(
                text="Далее ➡️",
                callback_data=f"next_page_{page + 1}"
            )
        )

    if page > 1:
        kb.add(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"prev_page_{page - 1}"
            )
        )

    try:
        await msg.edit_text("Вот список автомобилей:", reply_markup=kb.as_markup())
    except TelegramBadRequest:
        await msg.answer("Вот список автомобилей:", reply_markup=kb.as_markup())


async def car_details(call: CallbackQuery, db: AsyncSession):
    car_id = int(call.data.split('_')[1])

    car_crud = CarCRUD(db)
    car = await car_crud.get_car_by_id(car_id=car_id)

    if car:
        text = f"Информация о машине:\n\n" \
               f"Марка: {car.brand}\n" \
               f"Модель: {car.model}\n" \
               f"Год выпуска: {car.year}\n" \
               f"Цена: {car.price}₽\n"

        if car.photo_file_id:
            await call.message.edit_text(text)
            await call.message.answer_photo(car.photo_file_id)
        else:
            await call.message.edit_text(f"{text}\nФотография не доступна.")
    else:
        await call.answer("Машина не найдена.", show_alert=True)


async def paginate_cars(call: CallbackQuery, db: AsyncSession):
    page = int(call.data.split('_')[2])
    await list_cars(call.message, db, page)
    await call.answer()


def register_handlers_cars_list(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(list_cars, lambda msg: msg.text == "Список машин")
    dp.callback_query.register(car_details, lambda call: call.data.startswith("car_"))
    dp.callback_query.register(paginate_cars,
                               lambda call: call.data.startswith("next_page_") or call.data.startswith("prev_page_"))
    dp.include_router(router)
