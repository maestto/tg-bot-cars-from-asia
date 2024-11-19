from aiogram import Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton


async def main_menu(msg: Message):
    print(msg.chat.id)
    text = "🔹 Главное меню\n\nВыберите действие:"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить машину")],
            [KeyboardButton(text="Список машин")],
            [KeyboardButton(text="Найти машину")]
        ],
        resize_keyboard=True
    )
    await msg.answer(text=text, reply_markup=keyboard)


async def main_menu_callback(call: CallbackQuery):
    text = "🔹 Главное меню"
    await call.message.edit_text(text=text)
    await call.answer()


def register_handlers_base(dp: Dispatcher):
    router = Router(name=__name__)
    router.callback_query.register(main_menu_callback, F.data == "main_menu")
    dp.include_router(router)

