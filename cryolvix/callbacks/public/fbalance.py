from aiogram.types import CallbackQuery, InaccessibleMessage
from aiogram.utils.i18n import gettext as i18n

from cryolvix.core.userdata import UserData
from cryolvix.utils import old_format_num

async def fbalance(callback: CallbackQuery, user: UserData, **_ ):
    if (
        not callback.data or 
        not callback.message or
        isinstance(callback.message, InaccessibleMessage)
    ): return
    
    cuid = callback.data.split(":", 1)[1]
    if not cuid: return
    try:
        if int(cuid) != user.id:    
            await callback.answer(
                i18n("errors/not_your_button"),
                show_alert=True
            )
    except: return
    
    await callback.answer(
        f"{i18n("balance/callback/money").format(money=old_format_num(user.money))}\n"
        f"{i18n("balance/callback/crypto").format(crypto=old_format_num(user.cryocoins))}", 
        show_alert=True
    )
