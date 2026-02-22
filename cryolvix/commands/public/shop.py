from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.i18n import gettext as i18n
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.keyboard import InlineKeyboardBuilder

from cryolvix.config import EMOJIS, CustomInlineButton
from cryolvix.core.license import LICENSES
from cryolvix.database.repositories.product_repo import ProductRepository

async def shop(message: Message, product_repo: ProductRepository, bot: Bot, **_):
    gpus = await product_repo.get_shop_items()
    builder = InlineKeyboardBuilder()
    gpu_buttons = []
    license_buttons = []
    
    if gpus:
        for gpu in gpus:
            payload = f"product:{gpu.product_id[0]}:{gpu.product_id[1]}"
            if message.chat.type == "private":
                gpu_buttons.append(CustomInlineButton(
                    text=gpu.model,
                    callback_data=payload,
                    icon_custom_emoji_id=EMOJIS.CHIP.ID
                ))
            else:
                link = await create_start_link(bot, payload, True)
                gpu_buttons.append(CustomInlineButton(
                    text=gpu.model,
                    url=link,
                    icon_custom_emoji_id=EMOJIS.CHIP.ID
                ))
                
    if LICENSES:
        for license in LICENSES.values():
            if license.product_id[1] == 0: continue
            payload = f"product:{license.product_id[0]}:{license.product_id[1]}"
            if message.chat.type == "private":
                license_buttons.append(CustomInlineButton(
                    text=license.title,
                    callback_data=payload,
                    icon_custom_emoji_id=license.emoji.ID
                ))
            else:
                link = await create_start_link(bot, payload, True)
                license_buttons.append(CustomInlineButton(
                    text=license.title,
                    url=link,
                    icon_custom_emoji_id=license.emoji.ID
                ))
                
    builder.add(*gpu_buttons)
    builder.add(*license_buttons)
    builder.adjust(2)
    
    await message.reply(
        f"{EMOJIS.SHOP} {i18n("shop/title")}\n\n"
        f"{EMOJIS.YES} {i18n("shop/available")}\n"
        f"{EMOJIS.CHIP} {i18n("shop/gpus").format(gpus=len(gpu_buttons))}\n"
        f"{EMOJIS.LICENSE} {i18n("shop/licenses").format(licenses=len(license_buttons))}\n\n"
        f"{EMOJIS.DOWN} {i18n("shop/footer")}",
        reply_markup=builder.as_markup()
    )
