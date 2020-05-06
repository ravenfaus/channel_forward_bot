import logging

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

import config
import handlers


logging.basicConfig(level=logging.DEBUG)
storage = RedisStorage2(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, password=config.REDIS_PASS)
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
handlers.user.setup(dp)
handlers.channel.setup(dp)