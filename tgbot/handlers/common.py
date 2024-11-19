from aiogram import types, Dispatcher, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from services.crud.user import User as UserCrud
from handlers.main_menu import main_menu
from handlers.registration import start as registration_start


async def command_start(msg: types.Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    tg_id = msg.from_user.id

    user_crud = UserCrud(db=db)
    exists = await user_crud.user_exists(tg_id)

    if not exists:
        await registration_start(msg, state)
    else:
        await main_menu(msg)


async def set_admin_chat(msg: types.Message, db: AsyncSession, state: FSMContext):
    await msg.reply("Chat ID: " + str(msg.chat.id))


def register_handlers_common(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(command_start, Command("start"), StateFilter("*"))
    router.message.register(set_admin_chat, Command("chat"), StateFilter("*"))
    dp.include_router(router)
