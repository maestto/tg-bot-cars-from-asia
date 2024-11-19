from aiogram.fsm.state import StatesGroup, State


class CarForm(StatesGroup):
    brand = State()
    model = State()
    year = State()
    price = State()
    photo = State()