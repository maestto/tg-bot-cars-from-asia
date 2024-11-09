from aiogram import types, Dispatcher, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from services.crud.user import User as UserCrud
from handlers.main_menu import main_menu


async def command_start(msg: types.Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    user_crud = UserCrud(db=db)
    check = await user_crud.user_exists(msg.from_user.id)
    if not check:
        await user_crud.insert_user(user_tg_id=msg.from_user.id)
        await user_crud.commit()
    await main_menu(msg)


def register_handlers_common(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(command_start, Command("start"), StateFilter("*"))
    dp.include_router(router)
