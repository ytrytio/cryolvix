__all__ = ["router"]

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from typing import TypedDict
from cryolvix.commands import admin
from cryolvix.commands import public

class CommandOptions(TypedDict):
    prefix: str
    ignore_case: bool
    ignore_mention: bool

default_options: CommandOptions = {
    "prefix": "/!.",
    "ignore_case": True,
    "ignore_mention": False,
}

router = Router()

router.message.register(admin.update_shop, Command(commands=["update_shop"], **default_options))

router.message.register(public.start, Command(commands=["start"], **default_options))
router.message.register(public.balance, Command(commands=["cash", "balance"], **default_options))
router.message.register(public.rate, Command(commands=["rate", "cryocoin"], **default_options))
router.message.register(public.ping, Command(commands=["ping"], **default_options))
router.message.register(public.farming, Command(commands=["farming", "farm", "mine"], **default_options))
router.message.register(public.profile, Command(commands=["profile", "info"], **default_options))
router.message.register(public.shop, Command(commands=["shop", "store"], **default_options))
router.message.register(public.market, Command(commands=["market"], **default_options))
router.message.register(public.sell, Command(commands=["sell"], **default_options))
router.message.register(public.buy, Command(commands=["buy"], **default_options))
router.message.register(public.money_top, Command(commands=["mtop"], **default_options))
router.message.register(public.crypto_top, Command(commands=["ctop"], **default_options))
