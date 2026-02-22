from aiogram.types import CallbackQuery, InaccessibleMessage
from aiogram.utils.i18n import gettext as i18n

from cryolvix.core.product import Product
from cryolvix.database.repositories.product_repo import ProductRepository

async def product(callback: CallbackQuery, **_):
    if (
        not callback.data or 
        not callback.message or
        isinstance(callback.message, InaccessibleMessage)
    ): return
    product_id = callback.data.split(":", 1)[1]
    product = Product.from_id(product_id)
    
    if product:
        await callback.message.edit_text(
            text=product.text,
            reply_markup=product.keyboard
        )
    else:
        await callback.answer(i18n("product/not_found"), show_alert=True)
