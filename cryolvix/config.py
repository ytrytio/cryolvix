from aiogram.utils.i18n import I18n
from aiogram.types import InlineKeyboardButton

from pathlib import Path
from dotenv import dotenv_values
from typing import Dict

_secrets: Dict[str, str | None] = dotenv_values(".env")

BOT_TOKEN: str = _secrets.get("BOT_TOKEN") or ""
if not BOT_TOKEN: raise ValueError( "BOT_TOKEN not found in .env")
DATABASE_URL: str = _secrets.get("DATABASE_URL") or "postgresql+asyncpg://postgres:postgres@localhost:5432/cryolvix"
if not DATABASE_URL: raise ValueError( "DATABASE_URL not found in .env")

PROJECT_DIR = Path(__file__).parent.parent
TEMPLATE_SQL = PROJECT_DIR / "template.sql"
LOCALES = PROJECT_DIR / "locales"

UPDATE_TIME = 120
SUBSCRIPTION_TIME = MONTH = 2592000
ADMINS = [1432248216]

I18N = I18n(
    path=LOCALES,
    default_locale="en",
    domain="messages",
)

class PremiumEmoji:
    def __init__(self, emoji_id: int, emoji: str):
        self._id = emoji_id
        self._emoji = emoji

    def __str__(self) -> str:
        return f'<tg-emoji emoji-id="{self._id}">{self._emoji}</tg-emoji>'

    def __format__(self, format_spec) -> str:
        return str(self)

    def __getitem__(self, item):
        return (self._id, self._emoji)[item]
        
    @property
    def ID(self): return str(self._id)

class EMOJIS:
    LOADINGS = [
        PremiumEmoji(5316770651720137011, "🔘"),
        PremiumEmoji(5316930493223025689, "👾"),
        PremiumEmoji(5316575892133132571, "🚨"),
        PremiumEmoji(5316698440434989602, "✨"),
        PremiumEmoji(5377512995502960014, "❤️"),
        PremiumEmoji(5312467055834856065, "〽️"),
        PremiumEmoji(5377321160788684946, "❤️")
    ]
    
    GREETINGS = PremiumEmoji(5319007286004299794, "👋")
    BALANCE = BUY = PremiumEmoji(6030828420881976645, "💳")
    MONEY = PremiumEmoji(5316711376876485361, "💰")
    CRYPTOWALLET = PremiumEmoji(5316979275461573049, "👛")
    ROCKET = PremiumEmoji(5316571734604790521, "🚀")
    FLYING = PremiumEmoji(5377376720485626017, "❤️")
    UP = PremiumEmoji(5350305520144106741, "⏫")
    DOWN = PremiumEmoji(5350700390847365132, "⏬")
    EXCHANGE = PremiumEmoji(5350729313157135529, "💱")
    TOP = PremiumEmoji(5319290036586296571, "🔝")
    SNOWFLAKE = CRYOCOIN = PremiumEmoji(5316599316884766402, "❄️")
    LAMP = PremiumEmoji(5316637280100693932, "💡")
    TIME = PremiumEmoji(5316591603123502631, "⏰")
    LIGHTNING = PremiumEmoji(5251333384696776743, "⚡️")
    
    PONGS = [
        LIGHTNING,
        ROCKET,
        LAMP
    ]
    
    NO = PremiumEmoji(5348402067947929537, "🚫")
    SUCCESS = YES = PremiumEmoji(5251640796980988494, "✅")
    STAR = VIP = PremiumEmoji(5316692281451887373, "⭐️")
    PLUS = LIGHTNING
    DIZZY = ULTRA = PremiumEmoji(5348275460901977184, "💫")
    SUN = QUANTUM = PremiumEmoji(5348403541121713090, "☀️")
    
    MININGFARM = PremiumEmoji(5420093060757351136, "🪙")
    CHIP = PremiumEmoji(6019462434178211398, "📱")
    LICENSE = PremiumEmoji(6010311074346178283, "⭐️")
    
    PROFILE = PremiumEmoji(5260399854500191689, "👤")
    NAME = PremiumEmoji(5848355262137636971, "👾")
    ID = PremiumEmoji(5253577054137362120, "🔗")
    
    PRODUCT = PremiumEmoji(5317051834639071081, "💼")
    TYPE = PremiumEmoji(6028552122574835350, "⚙️")
    PRICE = PremiumEmoji(5890883384057533697, "🏷")
    LIMIT = PremiumEmoji(5208551133856945073, "❤️")
    
    WARNING = PremiumEmoji(5253864872780769235, "❗️")
    UPDATE = TOP = PremiumEmoji(5319290036586296571, "🔝")
    BACK = PremiumEmoji(5316635411789931847, "◀️")
    SHOP = PremiumEmoji(6030561664758191905, "🛒")
    
class CustomInlineButton(InlineKeyboardButton):
    style: str | None = "primary"

CMDS_LINK = "https://teletype.in/@cryolvix"
