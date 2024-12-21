import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from loguru import logger
from sqlalchemy.orm import close_all_sessions

from tgbot.middlewares.db import DBMiddleware
from tgbot.middlewares.media_group import MediaGroupMiddleware
from tgbot.models.config_reader import Settings
from tgbot.models.db.base import create_pool
from tgbot.utils import logging
from tgbot.utils.register_handlers import register_handlers


async def main():
    config = Settings()

    logging.setup(debug=config.debug_status())
    logger.warning("Starting bot..")

    bot_properties = DefaultBotProperties(parse_mode="html")
    bot = Bot(token=config.BOT_TOKEN.get_secret_value(),
              default=bot_properties
              )
    dp = Dispatcher(storage=RedisStorage.from_url(str(config.REDIS_DSN)))

    await bot.set_my_commands(commands=[BotCommand(command='start', description='Перезапустить бота')])

    db_pool = create_pool(str(config.PG_DSN), echo=config.debug_status())
    db_middleware = DBMiddleware(db_pool)
    dp.message.middleware(db_middleware)
    dp.callback_query.middleware(db_middleware)
    media_group_middleware = MediaGroupMiddleware()
    dp.message.middleware(media_group_middleware)

    register_handlers(dp)

    try:
        await dp.start_polling(bot,
                               allowed_updates=dp.resolve_used_update_types(),
                               config=config
                               )
    finally:
        await dp.storage.close()
        close_all_sessions()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
