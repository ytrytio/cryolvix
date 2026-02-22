from aiogram.types import Message
from aiogram.utils.i18n import gettext as i18n

from random import randint
from time import time as unixtime

from cryolvix.database.repositories.user_repo import UserRepository
from cryolvix.config import EMOJIS
from cryolvix.core.userdata import UserData
from cryolvix.core.economy import Economy
from cryolvix.core.license import License
from cryolvix.utils import format_num, format_time

def mine(hashrate: float, license: License) -> float:
    random_cash = int(randint(1000, 10000))
    random_cash *= license.multiplier
    random_cash *= hashrate if hashrate >= 1 else 1

    # random_cash *= perm_videocards if perm_videocards else 1
    # random_cash *= elite_videocards * 20 if elite_videocards else 1

    # random_cash += random_cash * row["boost"]

    result = Economy.bucks_to_crypto(random_cash)
    
    return round(result, 2)

async def farming(message: Message, user: UserData, user_repo: UserRepository, **_):
    now = unixtime()

    if now - user.cooldown < user.license.cooldown:
        remaining = user.license.cooldown - (now - user.cooldown)
        await message.reply(
            f"{EMOJIS.MININGFARM} {i18n("farming/title")}\n\n"
            f"{EMOJIS.WARNING} {i18n("farming/already")}\n"
            f"{EMOJIS.TIME} {i18n("farming/remaining").format(remaining=format_time(remaining))}\n\n"
            f"{EMOJIS.UPDATE} {i18n("farming/update")}"
        )
        return
    
    farmed = mine(user.hashrate, user.license)
    
    user.cryocoins += farmed
    user.cooldown = round(now)
    Economy.add_farmed(farmed)
    
    await user.update(repo=user_repo)
    await message.reply(
        f"{EMOJIS.MININGFARM} {i18n("farming/title")}\n\n"
        f"{EMOJIS.BALANCE} {i18n("farming/income").format(income=format_num(farmed))}\n"
        f"{user.license.emoji} {i18n("farming/license").format(license=user.license.title)}\n"
        f"{EMOJIS.CHIP} {i18n("farming/gpus").format(gpus=len(user.gpus))}\n"
        f"{EMOJIS.UP} {i18n("farming/multiplier").format(multiplier=user.hashrate + user.license.multiplier)}\n\n"
        f"{EMOJIS.EXCHANGE} {i18n("farming/footer")}"
    )
