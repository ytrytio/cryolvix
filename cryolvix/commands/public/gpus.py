from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as i18n

from cryolvix.config import EMOJIS, CustomInlineButton, GPUS_KB_LIMIT
from cryolvix.core.gpu import get_model, GPUModel
from cryolvix.core.userdata import UserData
from cryolvix.utils import pretty_print_structure as pps

def sort_gpus(gpus: list, owner: int, page: int = 1, limit: int = GPUS_KB_LIMIT) -> list:
    if limit <= 0: raise ValueError("limit must be a positive integer")

    result = []
    temp = []
    start = (page-1) * (limit-1)
    end = start + 10
    
    for gpu in gpus[start:end]:
        _model = get_model(
            company=gpu.company,
            prefix=gpu.prefix,
            series=gpu.series,
            level=gpu.level,
            suffix=gpu.suffix
        )
        gpumodel = GPUModel(
            model=_model,
            company=gpu.company,
            prefix=gpu.prefix,
            series=gpu.series,
            level=gpu.level,
            multiplier=gpu.multiplier,
            suffix=gpu.suffix
        )
        temp.append(
            [
                CustomInlineButton(
                    text=gpumodel.model,
                    callback_data=f"gpuinfo:{owner}:{gpumodel.product_id[0]}:{gpumodel.product_id[1]}"
                )
            ]
        )

        if len(temp) >= limit:
            for btn in temp: result.append(btn)
            temp = []

    if temp: 
        for btn in temp: 
            result.append(btn)
    return result


def get_keyboard(gpus: list, owner: int, page: int = 1):
    result = []
    buttons = sort_gpus(gpus, owner, page)
    if buttons:
        pps(buttons)
        result = buttons
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
        if len(gpus) - page * GPUS_KB_LIMIT > 0:
            sysrow.append(
                CustomInlineButton(
                    text=i18n("pages/next"), 
                    callback_data=f"gpuinfo:{owner}:page:{page+1}"
                )
            )
        result.append(sysrow)
    else:
        result.append(
            [
                CustomInlineButton(
                    text=i18n("gpus/shop"), 
                    callback_data="shop",
                    icon_custom_emoji_id=EMOJIS.BALANCE.ID
                )
            ]
        )
        
    pps(result)
    kb = InlineKeyboardMarkup(inline_keyboard=result)
    return kb

def get_text(user: UserData) -> str:
    text = (
        f"{EMOJIS.CHIP} {i18n("gpus/title")}\n\n"
        f"{EMOJIS.CHIP} {i18n("farming/gpus").format(gpus=len(user.gpus))}\n"
        f"{EMOJIS.UP} {i18n("farming/multiplier").format(multiplier=user.hashrate)}\n\n"
        f"{EMOJIS.DOWN} {i18n("gpus/footer/hasgpu") if user.gpus else i18n("gpus/footer/nogpu")}"
    )
    return text

async def gpus(message: Message, user: UserData, **_):
    markup = get_keyboard(user.gpus, user.id)
    text = get_text(user)

    await message.reply(
        text=text,
        reply_markup=markup
    )
