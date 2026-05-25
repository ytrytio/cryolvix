from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message
from aiogram.utils.i18n import gettext as i18n

from html import escape

from cryolvix.database.repositories.user_repo import UserRepository
from cryolvix.config import EMOJIS
from cryolvix.core.userdata import UserData
from cryolvix.utils import format_num

async def usage(
    message: Message, 
    reply: bool = False, 
    self: bool = False,
    noargs: bool = False,
    notenough: bool = False,
):
    text = f"{EMOJIS.TRANSACTION} {i18n("give/title")}\n"
    text += f"\n{EMOJIS.REPLY} {i18n("help/reply")}\n" if reply else ""
    text += f"\n{EMOJIS.STOP} {i18n("give/self")}\n" if self else ""
    text += f"\n{EMOJIS.NO} {i18n("give/noargs")}\n" if noargs else ""
    text += f"\n{EMOJIS.NO} {i18n("give/not_enough")}\n" if notenough else ""
    text += f"\n{EMOJIS.INFO} {i18n("help/usage")}\n"
    text += f"{EMOJIS.DASH} {i18n("give/usage")}"
    await message.reply(text)
    
async def give(message: Message, user: UserData, user_repo: UserRepository, command: CommandObject, bot: Bot, **_):
    replied = message.reply_to_message
    args = command.args
    
    if not args: return await usage(message, False, False, True)
    if not replied or not replied.from_user: return await usage(message, True)
    
    try:
        target = await UserData.create_or_load(replied.from_user, user_repo)
        botdata = await user_repo.get_by_id(bot.id)
        crypto = float(args.strip())
        
        if target.id == user.id:
            return await usage(message, False, True)
        if target.id == bot.id:
            return await usage(message)
        if crypto <= 0: 
            return await usage(message)
            
        fee = crypto * 0.01
        
        if user.cryocoins < crypto + fee:
            return await usage(message, False, False, False, True)
        else:
            user.cryocoins -= (crypto + fee)
            
        target.cryocoins += crypto
        await user.update(user_repo)
        await target.update(user_repo)
        
        if botdata is not None:
            await user_repo.update(bot.id, cryocoins=float(botdata.cryocoins)+fee)
    except: return await usage(message)
    
    await message.reply(
        f"{EMOJIS.TRANSACTION} {i18n("give/title")}\n\n"
        f"{EMOJIS.CRYPTOWALLET} {i18n("give/sender").format(name=user.shortlink)}\n"
        f"{EMOJIS.DOWN} {i18n("give/amount").format(amount=format_num(crypto))}\n"
        f"{EMOJIS.CRYPTOWALLET} {i18n("give/receiver").format(name=target.shortlink)}\n"
        f"{EMOJIS.FEE} {i18n("give/fee").format(fee=format_num(fee))}\n\n"
        f"{EMOJIS.SUCCESS} {i18n("give/success")}"
    )
