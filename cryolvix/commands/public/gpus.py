from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as i18n

from cryolvix.config import EMOJIS, CustomInlineButton
from cryolvix.core.userdata import UserData
from cryolvix.utils import format_num

def sort_gpus(gpus: list, owner: int, limit: int = 10) -> list:
    result = []
    temp = []
    for gpu in gpus:
        if len(temp) >= limit:
            result.append(temp)
            temp = []
        temp.append(
            [
                CustomInlineButton(
                    text=gpu.model, 
                    callback_data=f"gpuinfo:{owner}:{gpu.product_id[0]}:{gpu.product_id[1]}"
                )
            ]
        )
    return result

def get_keyboard(gpus: list, owner: int, page: int = 1):
    result = []
    buttons = sort_gpus(gpus, owner)
    if buttons:
        result.append(*buttons[page-1])
        sysrow = []
        if page - 1 > 0: 
            sysrow.append(
                CustomInlineButton(
                    text=i18n("pages/back"), 
                    callback_data=f"gpuinfo:{owner}:page:{page-1}",
                    icon_custom_emoji_id=EMOJIS.BACK.ID
                )
            )
            sysrow.append(
                CustomInlineButton(
                    text=str(page), 
                    callback_data=f"gpuinfo:{owner}:page:1"
                )
            )
        sysrow.append(
            CustomInlineButton(
                text=i18n("pages/next"), 
                callback_data=f"gpuinfo:{owner}:page:{page+1}"
            )
        )
        result.append(sysrow)
    else:
        result.append(
            CustomInlineButton(
                text=i18n("gpus/shop"), 
                callback_data="shop",
                icon_custom_emoji_id=EMOJIS.BALANCE.ID
            )
        )
    kb = InlineKeyboardMarkup(inline_keyboard=result)
    return kb

async def gpus(message: Message, user: UserData, **_):
    markup = get_keyboard(user.gpus, user.id)
    
    text = (
        f"{EMOJIS.CHIP} {i18n("gpus/title")}\n\n"
        f"{EMOJIS.CHIP} {i18n("farming/gpus").format(gpus=len(user.gpus))}\n"
        f"{EMOJIS.UP} {i18n("farming/multiplier").format(multiplier=user.hashrate)}\n\n"
        f"{EMOJIS.DOWN} {i18n("gpus/footer")}"
    )
    await message.reply(
        text=text,
        reply_markup=markup
    )
