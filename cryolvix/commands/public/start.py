from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters import CommandObject
from aiogram.utils.deep_linking import decode_payload
from aiogram.utils.i18n import gettext as i18n

from cryolvix.commands.public.profile import profile
from cryolvix.config import EMOJIS, CustomInlineButton, CMDS_LINK, SOURCE_CODE
from cryolvix.core.userdata import UserData
from cryolvix.core.product import Product
from cryolvix.database.models import User
from cryolvix.database.repositories.user_repo import UserRepository

async def start(message: Message, user: UserData, command: CommandObject, user_repo: UserRepository, **_):
    args = decode_payload(command.args) if command.args else None
    
    if args:
        parts = args.split(":", 1)
        try:
            match parts[0]:
                case 'product':
                    product = Product.from_id(parts[1])
                    if product:
                        await message.reply(
                            text=product.text,
                            reply_markup=product.keyboard
                        )
                        return
                case 'profile':
                    user_model = await user_repo.get_by_id(int(parts[1]))
                    if user_model:
                        userdata = UserData.from_model(user_model)
                        await profile(message, userdata, user_repo)
                        return
        except: pass

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                CustomInlineButton(
                    text=i18n("start/buttons/commands"),
                    url=CMDS_LINK,
                    icon_custom_emoji_id=EMOJIS.FLYING.ID
                )
            ],
            [
                CustomInlineButton(
                    text=i18n("start/buttons/source"),
                    url=SOURCE_CODE,
                    icon_custom_emoji_id=EMOJIS.GITHUB.ID
                )
            ]
        ]
    )
    await message.reply(
        f"{EMOJIS.GREETINGS} " + 
        i18n("start/welcome").format(name=user.link),
        reply_markup=keyboard
    )
