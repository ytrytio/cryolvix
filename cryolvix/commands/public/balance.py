from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as i18n

from cryolvix.config import EMOJIS, CustomInlineButton
from cryolvix.core.userdata import UserData
from cryolvix.utils import format_num

async def balance(message: Message, user: UserData, **_):
    text = (
        f"{EMOJIS.BALANCE} {i18n("balance/title")}\n\n"
        f"{EMOJIS.MONEY} {i18n("balance/money").format(money=format_num(user.money))}\n"
        f"{EMOJIS.CRYOCOIN} {i18n("balance/crypto").format(crypto=format_num(user.cryocoins))}\n\n"
        f"{EMOJIS.ROCKET} {i18n("balance/footer")}"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                CustomInlineButton(
                    text=i18n("balance/full"), 
                    callback_data=f"fbalance:{user.id}"
                )
            ]
        ]
    )
    await message.reply(
        text=text,
        reply_markup=keyboard
    )
