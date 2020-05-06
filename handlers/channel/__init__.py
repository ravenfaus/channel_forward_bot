from aiogram import Dispatcher
from aiogram import types
from .channels import channel_handler


def setup(dp: Dispatcher):
    # Channels
    dp.register_channel_post_handler(channel_handler, content_types=types.ContentType.ANY)
