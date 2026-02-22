from aiogram.types import Message
from aiogram.filters import CommandObject
from aiogram.utils.i18n import gettext as i18n

from cryolvix.config import EMOJIS
from cryolvix.core.economy import Economy
from cryolvix.core.userdata import UserData
from cryolvix.database.repositories import UserRepository
from cryolvix.utils import format_num

async def usage(message: Message):
    await message.reply(
        f"{EMOJIS.MARKET} {i18n("market/title")}\n\n"
        f"{EMOJIS.INFO} {i18n("help/usage")}\n"
        f"{EMOJIS.DASH} {i18n("market/body/c2m")}"
    )
    
async def sell(message: Message, user: UserData, user_repo: UserRepository, command: CommandObject, **_):
    args = command.args
        
    if not args: return await usage(message)
    
    try:
        crypto = float(args.strip())
        
        if user.cryocoins < crypto:
            money = Economy.crypto_to_bucks(user.cryocoins)
            crypto = user.cryocoins
            user.cryocoins = 0 
        else:
            money = Economy.crypto_to_bucks(crypto)
            user.cryocoins -= crypto
            
        user.money += money
        await user.update(user_repo)
        Economy.add_farmed(money)
    except:
        return await usage(message)
    
    await message.reply(
        f"{EMOJIS.MARKET} {i18n("market/title")}\n\n"
        f"{EMOJIS.CRYOCOIN} {i18n("market/sold").format(amount=format_num(round(crypto, 2)))}\n"
        f"{EMOJIS.MONEY} {i18n("market/got").format(amount=format_num(round(money, 2)))}"
    )
