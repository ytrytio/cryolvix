from sqlalchemy import select, update
from cryolvix.database.models.config import GlobalConfig

class Economy:
    DEFAULT_RATE: float = 100.0
    current_rate: float = DEFAULT_RATE
    _farmed_amount: float = 0.0

    @classmethod
    async def load(cls, session_pool):
        async with session_pool() as session: 
            result = await session.execute(
                select(GlobalConfig.value).where(GlobalConfig.key == "rate")
            )
            rate = result.scalar()
            
            if rate is not None:
                cls.current_rate = float(rate)
            else:
                from sqlalchemy import insert
                await session.execute(
                    insert(GlobalConfig).values(key="rate", value=cls.DEFAULT_RATE)
                )
                await session.commit()
                cls.current_rate = cls.DEFAULT_RATE

    @classmethod
    def get_rate(cls) -> float:
        return cls.current_rate

    @classmethod
    def add_farmed(cls, amount: float):
        cls._farmed_amount += amount

    @classmethod
    async def update_rate(cls, session_pool):
        course_change = cls._farmed_amount * 0.002
        max_course_change = cls.current_rate * 0.02
        course_change = min(max(course_change, -max_course_change), max_course_change)

        decay = cls.current_rate * 0.001 if cls._farmed_amount == 0 else 0
        cls.current_rate = round(max(1.0, cls.current_rate + course_change - decay), 2)
        cls._farmed_amount = 0.0

        async with session_pool() as session:
            await session.execute(
                update(GlobalConfig)
                .where(GlobalConfig.key == "rate")
                .values(value=cls.current_rate)
            )
            await session.commit()
        return cls.current_rate

    @staticmethod
    def crypto_to_bucks(value: float) -> float:
        return value * Economy.get_rate()
    
    @staticmethod
    def bucks_to_crypto(value: float) -> float:
        return value / Economy.get_rate()
