from aiogram.types import CallbackQuery

from cryolvix.core.userdata import UserData

async def commands(callback: CallbackQuery, user: UserData, **_):
    await callback.answer(text="HUI", show_alert=True)
