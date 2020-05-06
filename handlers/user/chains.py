from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import ChatNotFound, Unauthorized
from models.chain import Chain


class ChainOrder(StatesGroup):
    add_chain = State()


async def chain_command(message: types.Message):
    await ChainOrder.add_chain.set()
    await message.answer('Добавь меня в канал, в который я буду пересылать посты с других каналов.\n'
                         'Затем перешли оттуда любой пост, чтобы я сохранил информацию об этом канале.\n'
                         'Используй /cancel, чтобы отменить процесс добавления.')


async def add_chain(message: types.Message, state: FSMContext):
    if message.forward_from_chat:
        await message.answer('Сейчас я попробую добавить пост в канал и сразу же удалю. Одну секунду...')
        chat_id = message.forward_from_chat.id
        try:
            test_message = await message.bot.send_message(chat_id, 'Тестовое сообщение...', disable_notification=True)
            await test_message.delete()
            chain = Chain()
            chain.chat_id = chat_id
            chain.title = message.forward_from_chat.title
            chain.type = message.forward_from_chat.type
            await chain.create()
            await state.finish()
            await message.answer('Канал был добавлен. Используй /list, чтобы увидеть список добавленных каналов.')
        except ChatNotFound or Unauthorized:
            await message.answer('Я не могу ничего написать. Пожалуйста, проверь, добавлен ли я в канал и имею ли я'
                                 ' возможность постить сообщения.')
    else:
        await message.answer('Я не вижу пересланного сообщения. Попробуй еще раз.')


async def cancel_order(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Процесс отменен.')
