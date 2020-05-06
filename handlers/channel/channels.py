from aiogram import types

import config
from models import Chat


async def channel_handler(message: types.Message):
    chat = await Chat.query.where(Chat.chat_id == message.chat.id).gino.first()
    if chat:
        await message.forward(chat.forward_id)
        await message.bot.send_message(config.ADMIN_ID, f"Сообщение с канала {chat.title} было перенаправлено")