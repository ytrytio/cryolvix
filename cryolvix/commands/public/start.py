from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters import CommandObject
from aiogram.utils.deep_linking import decode_payload
from aiogram.utils.i18n import gettext as i18n

from cryolvix.config import EMOJIS, CustomInlineButton, CMDS_LINK
from cryolvix.core.userdata import UserData
from cryolvix.core.product import Product

async def start(message: Message, user: UserData, command: CommandObject, **_):
    args = decode_payload(command.args) if command.args else None
    
    if args:
        parts = args.split(":", 1)
        match parts[0]:
            case 'product':
                product = Product.from_id(parts[1])
                if product:
                    await message.reply(
                        text=product.text,
                        reply_markup=product.keyboard
                    )
                    return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                CustomInlineButton(
                    text=i18n("start/buttons/commands"),
                    url=CMDS_LINK,
                    icon_custom_emoji_id=EMOJIS.FLYING.ID
                )
            ]
        ]
    )
    await message.reply(
        f"{EMOJIS.GREETINGS} " + 
        i18n("start/welcome").format(name=user.link),
        reply_markup=keyboard
    )
