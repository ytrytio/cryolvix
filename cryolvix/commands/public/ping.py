from aiogram.types import Message
from aiogram.utils.i18n import gettext as i18n

from time import perf_counter
from random import choice

from cryolvix.config import EMOJIS
from cryolvix.utils import format_num

async def ping(message: Message, **_):
    start_time = perf_counter()
    
    pinging = await message.reply(f"{choice(EMOJIS.LOADINGS)} {i18n("ping/start")}")
    
    end_time = perf_counter()
    ping_ms = (end_time - start_time) * 1000
    
    await pinging.edit_text(
        f"{choice(EMOJIS.PONGS)} {i18n("ping/pong")}\n"
        f"{EMOJIS.TIME} {i18n("ping/delay").format(ms=format_num(ping_ms))}"
    )
