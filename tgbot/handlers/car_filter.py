from aiogram import Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from services.crud.car import CarCRUD
from states.car_filter import CarFilterForm

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select


async def start_filter(msg: Message, state: FSMContext):
    await msg.answer("Введите марку автомобиля или отправьте 'пусто', если не хотите указывать:")
    await state.set_state(CarFilterForm.brand)


async def process_filter_brand(msg: Message, state: FSMContext):
    brand = msg.text.strip() or "пусто"
    await state.update_data(brand=brand)
    await msg.answer("Введите модель автомобиля или отправьте 'пусто', если не хотите указывать:")
    await state.set_state(CarFilterForm.model)


async def process_filter_model(msg: Message, state: FSMContext):
    model = msg.text.strip() or "пусто"
    await state.update_data(model=model)
    await msg.answer("Введите год выпуска автомобиля или отправьте 'пусто':")
    await state.set_state(CarFilterForm.year)


async def process_filter_year(msg: Message, state: FSMContext):
    year = msg.text.strip()
    year = int(year) if year.isdigit() else "пусто"
    await state.update_data(year=year)
    await msg.answer("Введите максимальную цену автомобиля или отправьте 'пусто':")
    await state.set_state(CarFilterForm.price)


async def process_filter_price(msg: Message, state: FSMContext):
    price = msg.text.strip()
    price = float(price) if price.replace('.', '', 1).isdigit() else "пусто"
    await state.update_data(price=price)
    await msg.answer("Укажите дополнительные пожелания к автомобилю (текст) или отправьте 'пусто':")
    await state.set_state(CarFilterForm.notes)


async def process_filter_notes(msg: Message, state: FSMContext, db: AsyncSession):
    notes = msg.text.strip()
    await state.update_data(notes=notes)
    filters = await state.get_data()

    admin_chat_id = -4588244738 #!!!!!!!

    await msg.bot.send_message(
        chat_id=admin_chat_id,
        text=f"Фильтры клиента: {filters}"
    )

    await search_cars(filters, msg, state, db)


async def search_cars(filters: dict, msg: Message, state: FSMContext, db: AsyncSession):
    car_crud = CarCRUD(db)
    cars = await car_crud.filter_cars(filters)

    if cars:
        await send_car_list(msg, cars)
    else:
        await msg.answer("Нет автомобилей, соответствующих вашим фильтрам.")
    await state.clear()


async def send_car_list(msg: Message, cars: list, page: int = 1, per_page: int = 5):
    start = (page - 1) * per_page
    end = start + per_page
    cars_page = cars[start:end]

    if not cars_page:
        await msg.answer("Нет автомобилей на этой странице.")
        return

    builder = InlineKeyboardBuilder()
    for car in cars_page:
        builder.button(
            text=f"{car.brand} {car.model} ({car.year}) - {car.price}₽",
            callback_data=f"car_{car.id}"
        )

    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=f"cars_page_{page - 1}")
    if end < len(cars):
        builder.button(text="➡️ Вперед", callback_data=f"cars_page_{page + 1}")

    builder.adjust(1)
    await msg.answer("Список автомобилей:", reply_markup=builder.as_markup())


async def show_car_details(call: CallbackQuery, car_id: int, db: AsyncSession):
    car = CarCRUD(db)
    car = await car.get_car_by_id(car_id)
    if car:
        await call.message.answer_photo(
            photo=car.photo_file_id,
            caption=f"Модель: {car.brand} {car.model}\n"
                    f"Год: {car.year}\n"
                    f"Цена: {car.price}₽"
        )
    else:
        await call.message.answer("Машина не найдена.")


def register_car_filter_handlers(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(start_filter, Command("filter"))
    router.message.register(process_filter_brand, CarFilterForm.brand)
    router.message.register(process_filter_model, CarFilterForm.model)
    router.message.register(process_filter_year, CarFilterForm.year)
    router.message.register(process_filter_price, CarFilterForm.price)
    router.message.register(process_filter_notes, CarFilterForm.notes)
    router.callback_query.register(show_car_details, F.data.startswith("view_car_"))
    dp.include_router(router)
