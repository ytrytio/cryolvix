from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.i18n import gettext as i18n

from cryolvix.database.models import User
from cryolvix.database.repositories import GlobalRepository
from cryolvix.config import EMOJIS, CustomInlineButton
from cryolvix.utils import format_num

async def top_keyboard(users: list[User], bot: Bot, filter: str) -> InlineKeyboardMarkup:
    keyboard = []
    for i, user in enumerate(users, start=1):
        link = await create_start_link(bot, f"profile:{user.id}", True)
        value = float(user.cryocoins) if filter == "crypto" else float(user.money)
        сhar = "₡" if filter == "crypto" else "$"
        keyboard.append(
            [
                CustomInlineButton(
                    text=f"{user.name[:15]}{"..." if len(user.name) >= 15 else ""} - {format_num(round(value))}{сhar}",
                    url=link,
                    icon_custom_emoji_id=EMOJIS.NUMBERS[i].ID
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def money_top(message: Message, global_repo: GlobalRepository, bot: Bot, **_):
    top = await global_repo.get_top_by_balance()
    markup = await top_keyboard(top, bot, "money")
    await message.reply(
        f"{EMOJIS.STATS} {i18n("top/title")}\n\n"
        f"{EMOJIS.MONEY} {i18n("top/money")}\n\n"
        f"{EMOJIS.DOWN} {i18n("top/footer")}",
        reply_markup=markup
    )

async def crypto_top(message: Message, global_repo: GlobalRepository, bot: Bot, **_):
    top = await global_repo.get_top_by_cryocoins()
    markup = await top_keyboard(top, bot, "crypto")
    await message.reply(
        f"{EMOJIS.STATS} {i18n("top/title")}\n\n"
        f"{EMOJIS.CRYOCOIN} {i18n("top/crypto")}\n\n"
        f"{EMOJIS.DOWN} {i18n("top/footer")}",
        reply_markup=markup
    )
