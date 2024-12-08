from aiogram.fsm.state import StatesGroup, State


class CarResponse(StatesGroup):
    info = State()
    photo = State()
