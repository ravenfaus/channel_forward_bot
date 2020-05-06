from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import ChatNotFound, Unauthorized
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from models.chat import Chat
from models.chain import Chain


class ChatOrder(StatesGroup):
    add_chat = State()


chain_callback = CallbackData('list', 'id')
add_to_chain_callback = CallbackData('add', 'id')
remove_chain_callback = CallbackData('del', 'id')
remove_chat_callback = CallbackData('delc', 'id')


async def chains_list(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    for chain in await Chain.query.gino.all():
        kb.add(InlineKeyboardButton(chain.title, callback_data=chain_callback.new(id=chain.chat_id)))
    if kb.values:
        await message.answer('Ниже список каналов, в которые будут приходить посты.'
                             'Если хочешь подписать канал на другие, нажми на него.', reply_markup=kb)


async def chain_actions(clb: types.CallbackQuery, callback_data: dict):
    await clb.answer()
    chain = await Chain.query.where(Chain.chat_id == int(callback_data['id'])).gino.first()
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton('Подписать канал', callback_data=add_to_chain_callback.new(id=callback_data['id'])))
    kb.add(InlineKeyboardButton('Удалить канал', callback_data=remove_chain_callback.new(id=callback_data['id'])))
    chats = await Chat.query.where(Chat.forward_id == chain.chat_id).gino.all()
    if chats:
        for chat in chats:
            kb.add(InlineKeyboardButton(chat.title, callback_data=remove_chat_callback.new(id=chat.chat_id)))
    await clb.message.edit_text(f"Управление каналом {chain.title}\nПри выборе подписки она будет удалена.",
                                reply_markup=kb)


async def add_chat(clb: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await clb.answer()
    await ChatOrder.add_chat.set()
    await state.update_data(forward_id=callback_data['id'])
    await clb.message.answer('Добавь меня в канал с которого я буду пересылать посты, и пришли мне оттуда любой пост,'
                             ' чтобы я сохранил данные канала.')


async def add_chat_forward(message: types.Message, state: FSMContext):
    if message.forward_from_chat:
        answer_message = await message.answer('Сейчас я попробую добавить пост в канал и сразу же удалю.'
                                              ' Одну секунду...')
        chat_id = message.forward_from_chat.id
        try:
            test_message = await message.bot.send_message(chat_id, 'Тестовое сообщение...', disable_notification=True)
            await test_message.delete()
            chat = Chat()
            chat.forward_id = int((await state.get_data())['forward_id'])
            chat.chat_id = chat_id
            if chat.forward_id == chat.chat_id:
                await answer_message.edit_text('Я не могу подписать канал на самого себя... '
                                               'Попробуй еще раз, или прекрати процесс /cancel')
                return
            chat.title = message.forward_from_chat.title
            chat.type = message.forward_from_chat.type
            await chat.create()
            await state.finish()
            await answer_message.edit_text('Подписка на канал готова. Используй /list,'
                                           ' чтобы увидеть список добавленных каналов.')
        except ChatNotFound or Unauthorized:
            await answer_message.answer('Я не могу ничего написать. Пожалуйста, проверь, '
                                        'добавлен ли я в канал и имею ли я возможность постить сообщения.')
    else:
        await message.answer('Я не вижу пересланного сообщения. Попробуй еще раз.')


async def remove_chain(clb: types.CallbackQuery, callback_data: dict):
    await clb.answer()
    chain = await Chain.query.where(Chain.chat_id == int(callback_data['id'])).gino.first()
    title = chain.title
    await chain.delete()
    await clb.message.answer('Канал {} был удален.'.format(title))


async def remove_chat(clb: types.CallbackQuery, callback_data: dict):
    await clb.answer()
    chat = await Chat.query.where(Chat.chat_id == int(callback_data['id'])).gino.first()
    title = chat.title
    await chat.delete()
    await clb.message.answer('Подписка на канал {} была удален.'.format(title))
