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
        f"{EMOJIS.DASH} {i18n("market/body/m2c")}"
    )
    
async def buy(message: Message, user: UserData, user_repo: UserRepository, command: CommandObject, **_):
    args = command.args
        
    if not args: return await usage(message)
    
    try:
        crypto = float(args.strip())
        money = Economy.crypto_to_bucks(crypto)
        
        if user.money < money:
            result = Economy.bucks_to_crypto(user.money)
            money = user.money
            user.money = 0 
        else:
            result = Economy.bucks_to_crypto(money)
            user.money -= money
            
        user.cryocoins += result
        await user.update(user_repo)
        Economy.sub_farmed(money)
    except:
        return await usage(message)
    
    await message.reply(
        f"{EMOJIS.MARKET} {i18n("market/title")}\n\n"
        f"{EMOJIS.CRYOCOIN} {i18n("market/bought").format(amount=format_num(round(result, 2)))}\n"
        f"{EMOJIS.MONEY} {i18n("market/spent").format(amount=format_num(round(money, 2)))}"
    )
