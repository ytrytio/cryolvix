__all__ = ["router"]

from aiogram import Router, F

from cryolvix.callbacks import public

router = Router()

router.callback_query.register(public.commands, F.data.startswith("commands"))
router.callback_query.register(public.shop, F.data.startswith("shop"))
router.callback_query.register(public.product, F.data.startswith("product"))
router.callback_query.register(public.buy, F.data.startswith("buy"))
router.callback_query.register(public.fbalance, F.data.startswith("fbalance"))
