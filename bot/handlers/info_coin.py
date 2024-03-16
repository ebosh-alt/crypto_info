from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.config import bot
from bot.states import States
from bot.utils.CryptoMarket import CoinMarket
from bot.utils.GetMessage import get_mes
from bot import keyboards as kb

router = Router()


@router.callback_query(F.data == "names_coin")
async def inp_name(message: CallbackQuery):
    id = message.from_user.id
    coin_market = CoinMarket()
    text = get_mes("name_symbol_coin") + "\n"
    data = await coin_market.get_all_names()
    for coin in data:
        text += f"{coin.name}: {coin.symbol}\n"

    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=text,
                                reply_markup=kb.back_start_kb)


@router.callback_query(F.data == "find")
async def inp_name(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("input_name_coin"),
                                reply_markup=kb.back_start_kb)
    await state.set_state(States.find)
    await state.update_data(message_id=message.message.message_id)


@router.message(States.find)
async def get_name(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    name_coin = message.text
    coin_market = CoinMarket()
    coin = await coin_market.get_price_coin(name_coin)
    await message.delete()
    if coin is None:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text=get_mes("not_found_coin", name_coin=name_coin),
                                    reply_markup=kb.back_start_kb)

    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text=get_mes("coin_info",
                                                 name=coin.name,
                                                 symbol=coin.symbol,
                                                 price=coin.quote.price,
                                                 volume_24h=coin.quote.volume_24h,
                                                 volume_change_24h=coin.quote.volume_change_24h,
                                                 percent_change_1h=coin.quote.percent_change_1h,
                                                 percent_change_24h=coin.quote.percent_change_24h,
                                                 percent_change_7d=coin.quote.percent_change_7d,
                                                 percent_change_30d=coin.quote.percent_change_30d,
                                                 percent_change_60d=coin.quote.percent_change_60d,
                                                 percent_change_90d=coin.quote.percent_change_90d,
                                                 last_updated=coin.quote.last_updated),
                                    reply_markup=kb.back_start_kb)

        # await state.clear()


find_rt = router
