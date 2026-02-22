from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.i18n import SimpleI18nMiddleware

from cryolvix.database.engine import AsyncSessionLocal
from cryolvix.core.middlewares import DBSessionMiddleware, AntiFloodMiddleware
from cryolvix.routers import commands, callbacks, events
from cryolvix.config import BOT_TOKEN, I18N

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode="HTML",
        link_preview_is_disabled=True,
        allow_sending_without_reply=True
    )
)

dp = Dispatcher(bot=bot)
i18n_mw = SimpleI18nMiddleware(i18n=I18N)
antiflood = AntiFloodMiddleware(time_limit=0.5)

dp.update.outer_middleware(DBSessionMiddleware(AsyncSessionLocal))
dp.message.middleware(i18n_mw)
dp.message.middleware(antiflood)
dp.callback_query.middleware(i18n_mw)
dp.callback_query.middleware(antiflood)

dp.include_routers(commands.router, events.router, callbacks.router)
