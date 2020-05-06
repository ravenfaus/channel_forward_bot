from aiogram import Dispatcher
from aiogram import types
from aiogram.types import BotCommand

import config
from .chains import add_chain, chain_command, cancel_order
from .chains import ChainOrder
from .chats import chains_list, add_chat, chain_actions, remove_chain, add_chat_forward, ChatOrder, remove_chat, \
    remove_chat_callback
from .chats import chain_callback, add_to_chain_callback, remove_chain_callback


def setup(dp: Dispatcher):
    dp.register_message_handler(cancel_order, state='*', commands=['cancel'])
    dp.register_message_handler(set_commands)
    # Chats
    dp.register_message_handler(chains_list, commands='list')
    dp.register_callback_query_handler(chain_actions, chain_callback.filter())
    dp.register_callback_query_handler(add_chat, add_to_chain_callback.filter())
    dp.register_callback_query_handler(remove_chain, remove_chain_callback.filter())
    dp.register_callback_query_handler(remove_chat, remove_chat_callback.filter())
    dp.register_message_handler(add_chat_forward, state=ChatOrder.add_chat, content_types=types.ContentType.ANY)
    # Chains
    dp.register_message_handler(chain_command, commands='add')
    dp.register_message_handler(add_chain, state=ChainOrder.add_chain, content_types=types.ContentType.ANY)


async def set_commands(message: types.Message):
    if message.from_user.id == config.ADMIN_ID:  # Подставьте сюда свой Telegram ID
        commands = [BotCommand('add', 'Добавить канал, в который будут сохраняться сообщения'),
                    BotCommand('list', 'Вывести список каналов'),
                    BotCommand('cancel', 'Отменить процесс добавления')]
        await message.bot.set_my_commands(commands)
        await message.answer("Команды настроены.")