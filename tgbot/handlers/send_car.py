from typing import List

from aiogram import types, Dispatcher, Router, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaDocument
from sqlalchemy.ext.asyncio import AsyncSession

from services.crud.car_request import CarRequest
from states.car_response import CarResponse


async def send_car(msg: types.Message, state: FSMContext, command: CommandObject):
    await msg.answer("🔹 Напишите информацию о машине")
    await state.set_state(CarResponse.info)
    await state.update_data(car_request_id=int(command.args))


async def car_info_writen(msg: types.Message, state: FSMContext):
    if len(msg.text) > 1000:
        await msg.answer(text="🔹 Текст не должен превышать 1000 символов")
        return
    await state.update_data(car_info="🔹 Вариант машины:\n\n" + msg.text)
    await msg.answer("🔹 Пришлите фото машины")
    await state.set_state(CarResponse.photo)


async def photos_sent(message: Message, album: List[Message], db: AsyncSession, state: FSMContext):
    data = await state.get_data()
    group_elements = []
    first = True
    for element in album:
        if first:
            caption_kwargs = {"caption": data['car_info']}
            first = False
        else:
            caption_kwargs = {"caption": element.caption, "caption_entities": element.caption_entities}
        if element.photo:
            input_media = InputMediaPhoto(media=element.photo[-1].file_id, **caption_kwargs)
        elif element.video:
            input_media = InputMediaVideo(media=element.video.file_id, **caption_kwargs)
        elif element.document:
            input_media = InputMediaDocument(media=element.document.file_id, **caption_kwargs)
        else:
            return message.answer("Данный тип медиа не поддерживается!")
        group_elements.append(input_media)

    car_req_crud = CarRequest(db=db)
    car_request = await car_req_crud.get_car_request(cr_id=data['car_request_id'])
    await message.bot.send_media_group(chat_id=car_request.tg_id, media=group_elements)
    await message.answer("Вариант отправлен! ✅")
    await state.clear()


def register_handlers_send_car(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(send_car, Command("start", magic=F.args), StateFilter("*"))
    router.message.register(car_info_writen, F.text, CarResponse.info)
    router.message.register(photos_sent, F.media_group_id, CarResponse.photo)
    dp.include_router(router)
