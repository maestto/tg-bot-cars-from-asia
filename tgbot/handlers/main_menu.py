from aiogram import Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def main_menu(msg: Message):
    text = "🔹 Главное меню\n\nВыберите действие:"
    kb = InlineKeyboardBuilder()
    kb.button(text="Запрос авто", callback_data="car_request")
    kb.button(text="Мои запросы", callback_data="my_car_requests")
    kb.adjust(1, 1)
    await msg.answer(text=text, reply_markup=kb.as_markup())


async def main_menu_callback(call: CallbackQuery):
    text = "🔹 Главное меню\n\nВыберите действие:"
    kb = InlineKeyboardBuilder()
    kb.button(text="Запрос авто", callback_data="car_request")
    kb.button(text="Мои запросы", callback_data="my_car_requests")
    kb.adjust(1, 1)
    await call.message.edit_text(text=text)
    await call.answer()


def register_handlers_base(dp: Dispatcher):
    router = Router(name=__name__)
    router.callback_query.register(main_menu_callback, F.data == "main_menu")
    dp.include_router(router)

