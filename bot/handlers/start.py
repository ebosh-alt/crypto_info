from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.config import bot
from bot.utils.GetMessage import get_mes
from bot import keyboards as kb

router = Router()


@router.callback_query(F.data == "start")
@router.message(Command("start"))
async def greeting_user(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.clear()

    if type(message) is CallbackQuery:
        await bot.delete_message(chat_id=id,
                                 message_id=message.message.message_id)

    if message.from_user.username is None:
        username = message.from_user.first_name
    else:
        username = f"@{message.from_user.username}"
    await bot.send_message(chat_id=id,
                           text=get_mes("start", username=username),
                           reply_markup=kb.start_kb)


start_rt = router
