from aiogram import types, Dispatcher, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.handlers.main_menu import main_menu
from tgbot.services.crud.user import User as UserCrud
from tgbot.states.registration import Registration


async def start(msg: types.Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Поделиться номером", request_contact=True)]
        ],
        resize_keyboard=True
    )
    await msg.answer("Пожалуйста, поделитесь своим номером телефона:", reply_markup=keyboard)
    await state.set_state(Registration.waiting_for_phone_number)


async def handle_phone_number(msg: types.Message, state: FSMContext):
    contact = msg.contact
    if contact:
        await state.update_data(tg_id=contact.user_id, phone_number=contact.phone_number)
        await msg.answer("Введите, пожалуйста, ваше ФИО:")
    await state.set_state(Registration.waiting_for_name)


async def handle_name(msg: types.Message, db: AsyncSession, state: FSMContext):
    name = msg.text

    data = await state.get_data()
    tg_id = data["tg_id"]
    phone_number = data["phone_number"]

    user_crud = UserCrud(db=db)

    await user_crud.insert_user(tg_id=tg_id, phone_number=phone_number, name=name)
    await user_crud.commit()
    await msg.answer("Регистрация завершена! Спасибо.")
    await main_menu(msg)
    await state.clear()


def register_handlers_registration(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(handle_phone_number, F.contact, Registration.waiting_for_phone_number)
    router.message.register(handle_name, F.text, Registration.waiting_for_name)
    dp.include_router(router)
