from aiogram.fsm.state import StatesGroup, State


class CarFilterForm(StatesGroup):
    brand = State()
    model = State()
    year = State()
    price = State()
    notes = State()
    additional_details = State()
