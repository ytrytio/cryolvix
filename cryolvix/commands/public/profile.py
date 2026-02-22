from aiogram.types import Message
from aiogram.utils.i18n import gettext as i18n

from html import escape

from cryolvix.database.repositories.user_repo import UserRepository
from cryolvix.config import EMOJIS
from cryolvix.core.userdata import UserData
from cryolvix.utils import format_num

async def profile(message: Message, user: UserData, user_repo: UserRepository, **_):
    replied = message.reply_to_message
    target = await UserData.create_or_load(replied.from_user, user_repo) if replied and replied.from_user else user
    await message.reply(
        f"{EMOJIS.PROFILE} {i18n("profile/title")}\n\n"
        f"{EMOJIS.NAME} {i18n("profile/name").format(name=escape(target.name))}\n"
        f"{EMOJIS.ID} {i18n("profile/id").format(id=target.id)}\n\n"
        f"{EMOJIS.MONEY} {i18n("balance/money").format(money=format_num(target.money))}\n"
        f"{EMOJIS.CRYOCOIN} {i18n("balance/crypto").format(crypto=format_num(target.cryocoins))}\n\n"
        f"{EMOJIS.CHIP} {i18n("farming/gpus").format(gpus=len(target.gpus))}\n"
        f"{user.license.emoji} {i18n("farming/license").format(license=target.license.title)}\n"
        f"{EMOJIS.UP} {i18n("farming/multiplier").format(multiplier=target.hashrate + target.license.multiplier)}"
    )
