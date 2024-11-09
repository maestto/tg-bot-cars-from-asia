from aiogram import Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def main_menu(msg: Message):
    text = "🔹 Главное меню"
    await msg.answer(text=text)


async def main_menu_callback(call: CallbackQuery):
    text = "🔹 Главное меню"
    await call.message.edit_text(text=text)
    await call.answer()


def register_handlers_base(dp: Dispatcher):
    router = Router(name=__name__)
    router.callback_query.register(main_menu_callback, F.data == "main_menu")
    dp.include_router(router)

