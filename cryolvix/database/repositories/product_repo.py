from sqlalchemy import select, delete
from cryolvix.database.models.product import Product
from cryolvix.core.gpu import GPUModel

class ProductRepository:
    def __init__(self, session):
        self.session = session

    async def get_shop_items(self) -> list[GPUModel]:
        result = await self.session.execute(select(Product))
        db_products = result.scalars().all()
        
        items = []
        for p in db_products:
            gpu_obj = GPUModel.from_id(p.product_id)
            if gpu_obj:
                items.append(gpu_obj)
        return items

    async def refresh_catalog(self, new_gpu_objects: list[GPUModel]):
        await self.session.execute(delete(Product))
        for i, gpu in enumerate(new_gpu_objects, start=1):
            raw_id = gpu.product_id[1]
            
            new_item = Product(
                slot=int(i),
                product_id=raw_id
            )
            self.session.add(new_item)
        await self.session.commit()
