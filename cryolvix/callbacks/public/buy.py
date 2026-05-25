from aiogram.types import CallbackQuery, InaccessibleMessage
from aiogram.utils.i18n import gettext as i18n

from cryolvix.core.product import Product
from cryolvix.core.userdata import UserData
from cryolvix.database.repositories import ProductRepository, GPURepository, UserRepository

async def buy(
    callback: CallbackQuery, 
    user: UserData, 
    user_repo: UserRepository,
    gpu_repo: GPURepository,
    product_repo: ProductRepository,
    **_
):
    if (
        not callback.data or 
        not callback.message or
        isinstance(callback.message, InaccessibleMessage)
    ): return
    
    product_id = callback.data.split(":", 1)[1]
    product = Product.from_id(product_id)
    
    if product:
        result = await product.buy(
            user=user, 
            user_repo=user_repo, 
            gpu_repo=gpu_repo,
            product_repo=product_repo
        )
    else: 
        result = i18n("product/not_found")
        
    await callback.answer(result, show_alert=True)
