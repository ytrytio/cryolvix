from aiogram.types import Message
from aiogram.utils.i18n import gettext as i18n

from cryolvix.config import EMOJIS
from cryolvix.core.economy import Economy
from cryolvix.utils import format_num

async def rate(message: Message, **_):
    rate = Economy.get_rate()
    await message.reply(
        f"{EMOJIS.EXCHANGE} {i18n("rate/title")}\n\n"
        f"{EMOJIS.CRYOCOIN} {i18n("rate/currency").format(rate=format_num(round(rate, 2)))}\n\n"
        f"{EMOJIS.LIGHTNING} {i18n("rate/footer")}"
    )
