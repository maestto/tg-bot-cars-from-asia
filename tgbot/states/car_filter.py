from aiogram.fsm.state import StatesGroup, State


class CarFilterForm(StatesGroup):
    car_info = State()
    price = State()
    additional_details = State()
