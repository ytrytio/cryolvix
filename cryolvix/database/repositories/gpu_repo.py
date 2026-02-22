from sqlalchemy import update

from time import time as unixtime
from typing import Optional

from cryolvix.database.models.gpu import GPU
from cryolvix.core.gpu import GPUModel

class GPURepository:
    def __init__(self, session):
        self.session = session

    async def add_gpu(self, user_id: int, gpu_obj: GPUModel):
        new_gpu = GPU(
            owner=user_id,
            created=int(unixtime()),
            company=gpu_obj.company,
            prefix=gpu_obj.prefix,
            series=gpu_obj.series,
            level=gpu_obj.level,
            suffix=gpu_obj.suffix,
            multiplier=int(gpu_obj.multiplier),
            working=True,
            wearout=0
        )
        self.session.add(new_gpu)
        await self.session.commit()
        return new_gpu

    async def apply_wearout(self, amount: int = 1):
        await self.session.execute(
            update(GPU)
            .where(GPU.working == True)
            .values(wearout=GPU.wearout + amount)
        )
        await self.session.execute(
            update(GPU)
            .where(GPU.wearout >= 100)
            .values(working=False)
        )
        await self.session.commit()
