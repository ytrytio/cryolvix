from aiogram.types import CallbackQuery, InaccessibleMessage
from aiogram.utils.i18n import gettext as i18n

from logging import getLogger

from cryolvix.config import GPUS_KB_LIMIT
from cryolvix.core.product import Product
from cryolvix.core.userdata import UserData
from cryolvix.commands.public.gpus import get_keyboard as get_gpus_keyboard, get_text as get_gpus_text
from cryolvix.database.repositories import GPURepository, UserRepository

logger = getLogger()

async def gpuinfo(
    callback: CallbackQuery, 
    user: UserData, 
    user_repo: UserRepository,
    gpu_repo: GPURepository,
    **_
):
    if (
        not callback.data or 
        not callback.message or
        isinstance(callback.message, InaccessibleMessage)
    ): return
    
    user_id = callback.data.split(":")[1]
    try:
        if user.id != int(user_id):
            await callback.answer(i18n("errors/not_your_button"), show_alert=True)
            return
        
        option = callback.data.split(":")[2]
        value = str(callback.data.split(":")[3])
            
        match option:
            case "gpu":
                gpu = Product.from_id("gpu:" + value)
                if gpu:
                    await callback.message.edit_text(
                        text=gpu.text,
                        reply_markup=gpu.custom_keyboard(f"gpuinfo:{user_id}:page:1")
                    )
                else:
                    await callback.answer(i18n("product/not_found"), show_alert=True)
            case "page":
                if int(value) * GPUS_KB_LIMIT - len(user.gpus) >= 10:
                    keyboard = get_gpus_keyboard(user.gpus, user.id)
                else:
                    keyboard = get_gpus_keyboard(user.gpus, user.id, int(value))
                text = get_gpus_text(user)
                await callback.message.edit_text(
                    text=text,
                    reply_markup=keyboard
                )
            case _:
                await callback.answer(i18n("errors/unknown"), show_alert=True)
                return
    except Exception as e:
        logger.error(e)
        await callback.answer(i18n("errors/unknown"), show_alert=True)
        return
