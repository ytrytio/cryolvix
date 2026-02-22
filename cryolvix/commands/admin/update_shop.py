from aiogram.types import Message, ReactionTypeEmoji
from aiogram.utils.i18n import gettext as i18n

from cryolvix.config import EMOJIS, ADMINS
from cryolvix.core.gpu import NoVideoGPU, GNDGPU
from cryolvix.core.userdata import UserData
from cryolvix.database.repositories.product_repo import ProductRepository

async def update_shop(message: Message, user: UserData, product_repo: ProductRepository, **_):
    if user.id not in ADMINS: return
    new_inventory = [
        NoVideoGPU.generate(),
        GNDGPU.generate(),
        NoVideoGPU.generate(),
        GNDGPU.generate()
    ]
    
    await product_repo.refresh_catalog(new_inventory)
    await message.react(reaction=[ReactionTypeEmoji(emoji="👌")])
