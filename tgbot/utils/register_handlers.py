from tgbot.handlers.car_filter import register_car_filter_handlers
from tgbot.handlers.common import register_handlers_common
from tgbot.handlers.registration import register_handlers_registration
from tgbot.handlers.main_menu import register_handlers_base
from tgbot.handlers.send_car import register_handlers_send_car


def register_handlers(dp):
    register_handlers_send_car(dp)
    register_handlers_common(dp)
    register_handlers_registration(dp)
    register_handlers_base(dp)
    register_car_filter_handlers(dp)
