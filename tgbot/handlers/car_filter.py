from aiogram import Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.models.config_reader import Settings
from tgbot.states.car_filter import CarFilterForm


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


async def process_filter_notes(msg: Message, state: FSMContext):
    notes = msg.text.strip()
    await state.update_data(notes=notes)
    filters = await state.get_data()

    config = Settings()
    admin_chat_id = config.ADMIN_CHAT_ID

    await msg.bot.send_message(
        chat_id=admin_chat_id,
        text=f"Фильтры клиента\n\n"
             f"Марка: {filters['brand']}\n"
             f"Модель: {filters['model']}\n"
             f"Год выпуска: {filters['year']}\n"
             f"Цена: {filters['price']}\n"
             f"Дополнительно: {filters['notes']}\n"
    )
    await msg.answer("Ваш запрос отправлен, скоро вам будут предложены варианты")


def register_car_filter_handlers(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(start_filter, Command("filter"))
    router.message.register(start_filter, F.text == "Найти машину")
    router.message.register(process_filter_brand, CarFilterForm.brand)
    router.message.register(process_filter_model, CarFilterForm.model)
    router.message.register(process_filter_year, CarFilterForm.year)
    router.message.register(process_filter_price, CarFilterForm.price)
    router.message.register(process_filter_notes, CarFilterForm.notes)
    dp.include_router(router)
