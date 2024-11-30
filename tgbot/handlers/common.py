from aiogram import types, Dispatcher, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.handlers.main_menu import main_menu
from tgbot.handlers.registration import start as registration_start
from tgbot.services.crud.user import User as UserCrud


async def command_start(msg: types.Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    tg_id = msg.from_user.id

    user_crud = UserCrud(db=db)
    exists = await user_crud.user_exists(tg_id)

    if not exists:
        await registration_start(msg, state)
    else:
        await main_menu(msg)


def register_handlers_common(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(command_start, Command("start"), StateFilter("*"))
    dp.include_router(router)
