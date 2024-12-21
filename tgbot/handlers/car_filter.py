from aiogram import Router, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.config_reader import Settings
from tgbot.services.crud.car_request import CarRequest
from tgbot.services.crud.user import User as UserCrud
from tgbot.states.car_filter import CarFilterForm


async def start_filter(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("🔹 Введите марку, модель и год интересующего автомобиля")
    await state.set_state(CarFilterForm.car_info)
    await call.answer()


async def car_info_writen(msg: Message, state: FSMContext):
    car_info = msg.text
    await state.update_data(car_info=car_info)
    await msg.answer("🔹 Введите ваш бюджет")
    await state.set_state(CarFilterForm.price)


async def process_filter_price(msg: Message, state: FSMContext):
    price = msg.text
    await state.update_data(price=price)
    await msg.answer("🔹 Укажите дополнительные пожелания к автомобилю")
    await state.set_state(CarFilterForm.additional_details)


async def process_filter_notes(msg: Message, db: AsyncSession, state: FSMContext, config: Settings):
    additional_details = msg.text
    data = await state.update_data(additional_details=additional_details)
    car_req_crud = CarRequest(db=db)
    req_obj = car_req_crud.insert_car_request(tg_id=msg.from_user.id,
                                              car_info=data['car_info'],
                                              price=data['price'],
                                              additional_details=additional_details,
                                              )
    await db.commit()
    await db.refresh(req_obj)
    kb = InlineKeyboardBuilder()
    kb.button(text="Отправить вариант ⬆️",
              url=f"tg://resolve?domain={config.BOT_USERNAME}&start={req_obj.id}")
    user_crud = UserCrud(db=db)
    user = await user_crud.get_user(msg.from_user.id)
    await msg.bot.send_message(
        chat_id=config.ADMIN_CHAT_ID,
        text=f"🔹 Запрос клиента\n"
             f"<b>ФИО:</b> {user.full_name}\n"
             f"<b>Номер телефона:</b> <code>{user.phone_number}</code>\n\n"
             f"<b>Данные по авто:</b> {data['car_info']}\n"
             f"<b>Цена:</b> {data['price']}\n"
             f"<b>Дополнительно:</b> {additional_details}\n",
        reply_markup=kb.as_markup()
    )
    await msg.answer("✅ Ваш запрос отправлен, скоро вам будут предложены варианты")


def register_car_filter_handlers(dp: Dispatcher):
    router = Router(name=__name__)
    router.callback_query.register(start_filter, F.data == "car_request")
    router.message.register(car_info_writen, CarFilterForm.car_info)
    router.message.register(process_filter_price, CarFilterForm.price)
    router.message.register(process_filter_notes, CarFilterForm.additional_details)
    dp.include_router(router)
