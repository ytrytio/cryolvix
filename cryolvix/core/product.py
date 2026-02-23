from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as i18n

from typing import Optional, Any

from cryolvix.core.userdata import UserData
from cryolvix.database.repositories.user_repo import UserRepository    
from cryolvix.config import EMOJIS, CustomInlineButton
from cryolvix.utils.utils import format_num, format_time
from .license import License, LICENSES, NoLicense
from .gpu import GPUModel

class Product:
    def __init__(
        self,
        name: str,
        product: License | GPUModel
    ) -> None:
        self.name = name 
        self.product = product
        
    @staticmethod
    def from_id(id: str) -> Optional["Product"]:
        product = None
        try:
            parts = id.split(":")
            ptype = parts[0]
            obj = None
            name = None
            if ptype == 'license':
                obj = LICENSES.get(int(parts[1]), NoLicense)
                name = obj.title
            elif ptype == 'gpu':
                obj = GPUModel.from_id(parts[1])
                assert obj is not None
                name = obj.model
            else: return product
            product = Product(
                name=name,
                product=obj
            )
        except: pass
        finally: return product
        
    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    CustomInlineButton(
                        text=i18n("product/buy"), 
                        callback_data=f"buy:{self.product.product_id[0]}:{self.product.product_id[1]}",
                        icon_custom_emoji_id=EMOJIS.BUY.ID
                    )
                ],
                [
                    CustomInlineButton(
                        text=i18n("product/back"), 
                        callback_data="shop",
                        icon_custom_emoji_id=EMOJIS.BACK.ID
                    )
                ],
            ]
        )
    
    @property
    def category(self) -> Optional[str]:
        if isinstance(self.product, License):
            return "license"
        elif isinstance(self.product, GPUModel):
            return "gpu"
        else:
            return "none"
        
    @property
    def text(self) -> str:
        text = f"{EMOJIS.PRODUCT} {i18n("product/title")}\n\n"
        text += f"{EMOJIS.TYPE} {i18n("product/type").format(type=i18n(f"types/{self.category}"))}\n"
        text += f"{EMOJIS.NAME} {i18n("product/name").format(title=self.name)}\n"
        if isinstance(self.product, License):
            text += f"{EMOJIS.LIMIT} {i18n("product/license/limit").format(limit=self.product.limit)}\n"
            text += f"{EMOJIS.TIME} {i18n("product/license/cooldown").format(cooldown=format_time(self.product.cooldown))}\n"
        text += f"{EMOJIS.UP} {i18n("product/multiplier").format(multiplier=self.product.multiplier)}\n\n"
        text += f"{EMOJIS.PRICE} {i18n("product/price").format(price=format_num(self.product.price))}\n"
        return text
        
    async def buy(self, user: "UserData", user_repo: "UserRepository", gpu_repo: Optional[Any] = None) -> str:
        if isinstance(self.product, License) and isinstance(user.license, License):
            index = self.product.product_id[1]
            if user.license.product_id[1] > index:
                return i18n("product/license/lower")
            elif user.license.product_id[1] == index:
                return i18n("product/license/even")
                
            if user.money < self.product.price:
                return i18n("product/no_money")
                
            user.license = self.product
            user.money -= self.product.price
            await user.update(user_repo)
            return i18n(f"product/{self.category}/success").format(title=self.product.title, price=format_num(self.product.price))
            
        elif isinstance(self.product, GPUModel):
            if user.money < self.product.price:
                return i18n("product/no_money")
            if user.license.limit <= len(user.gpus):
                return i18n(f"product/gpu/limit")
            if not gpu_repo:
                return i18n("product/not_found")
                
            await gpu_repo.add_gpu(user_id=user.id, gpu_obj=self.product)

            user.money -= self.product.price
            await user.update(user_repo)

            return i18n(f"product/{self.category}/success").format(title=self.product.model, price=format_num(self.product.price))
            
        else: return i18n("product/not_found")
