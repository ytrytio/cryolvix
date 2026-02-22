import sys
from logging import Logger

from cryolvix.utils.logger import setup_logger

logger: Logger = setup_logger()

class ImportLogger:
    def find_spec(self, fullname, *_, **__):
        if fullname.startswith(__package__):
            logger.info(f"Loading module: {fullname}")
        return None

sys.meta_path.insert(0, ImportLogger())
logger.info("Initializing system components...")

from asyncio import (
    run as aiorun, 
    sleep as asleep, 
    CancelledError, 
    create_task
)
from datetime import datetime, timedelta

from cryolvix.config import UPDATE_TIME
from cryolvix.core.bot import bot, dp
from cryolvix.core.gpu import NoVideoGPU, GNDGPU
from cryolvix.core.economy import Economy
from cryolvix.database.repositories.product_repo import ProductRepository
from cryolvix.database.session import AsyncSessionLocal

async def shop_update_loop(session_pool):
    try:
        while True:
            now = datetime.now()
            tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
            seconds_until_midnight = (tomorrow - now).total_seconds()
            
            logger.info(f"Shop update scheduled in {seconds_until_midnight/3600:.2f} hours")
            
            await asleep(seconds_until_midnight)
            
            async with session_pool() as session:
                product_repo = ProductRepository(session)
                
                new_inventory = [
                    NoVideoGPU.generate(),
                    GNDGPU.generate(),
                    NoVideoGPU.generate(),
                    GNDGPU.generate()
                ]
                
                await product_repo.refresh_catalog(new_inventory)
                logger.info("Shop inventory has been refreshed for the new day!")
                
    except CancelledError:
        logger.info("Shop update loop stopped.")

async def rate_update_loop(session_pool):
    try:
        while True:
            await asleep(120)
            new_rate = await Economy.update_rate(session_pool)
            logger.info(f"CryoCoin rate updated: {new_rate:.2f}")
    except CancelledError:
        pass 

async def main():
    session_pool = AsyncSessionLocal
    await Economy.load(session_pool)
    background_task = create_task(rate_update_loop(session_pool))
    try:
        await dp.start_polling(bot)
    finally:
        background_task.cancel()
        try:
            await background_task
        except CancelledError:
            pass

if __name__ == "__main__":
    aiorun(main())
