from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    waiting_for_phone_number = State()
    waiting_for_name = State()