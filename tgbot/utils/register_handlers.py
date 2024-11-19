from handlers.car_filter import register_car_filter_handlers
from handlers.common import register_handlers_common
from handlers.main_menu import register_handlers_base
from handlers.add_car import register_handlers_add_car
from handlers.cars_list import register_handlers_cars_list


def register_handlers(dp):
    register_handlers_common(dp)
    register_handlers_base(dp)
    register_handlers_add_car(dp)
    register_handlers_cars_list(dp)
    register_car_filter_handlers(dp)
