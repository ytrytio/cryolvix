from cryolvix.config import PremiumEmoji, EMOJIS
# from cryolvix.core.product import Product

class License:
    def __init__(
        self, 
        title: str, 
        cooldown: int,
        limit: int, 
        price: int, 
        multiplier: float,
        emoji: PremiumEmoji,
        starter: bool = False,
    ):
        self.title: str = title
        self.cooldown: int = cooldown
        self.limit: int = limit
        self.price: int = price
        self.multiplier: float = multiplier
        self.emoji: PremiumEmoji = emoji
        self.starter: bool = starter
        
    @property
    def product_id(self) -> tuple:
        uid = next((k for k, v in LICENSES.items() if v == self), 0)
        return ("license", uid)

NoLicense = License(
    title="FREE", 
    cooldown=7200, 
    limit=10, 
    price=0,
    multiplier=1,
    emoji=EMOJIS.NO,
    starter=True
)

VipLicense = License(
    title="VIP", 
    cooldown=3600, 
    limit=50, 
    price=1000000,
    multiplier=2,
    emoji=EMOJIS.VIP
)

PlusLicense = License(
    title="PLUS", 
    cooldown=1800, 
    limit=100, 
    price=10000000,
    multiplier=4,
    emoji=EMOJIS.PLUS
)

UltraLicense = License(
    title="ULTRA", 
    cooldown=1800, 
    limit=150, 
    price=100000000,
    multiplier=5,
    emoji=EMOJIS.ULTRA
)

QuantumLicense = License(
    title="QUANTUM", 
    cooldown=1800, 
    limit=200, 
    price=1000000000,
    multiplier=8,
    emoji=EMOJIS.QUANTUM
)

LICENSES = {
    0: NoLicense,
    1: VipLicense,
    2: PlusLicense,
    3: UltraLicense,
    4: QuantumLicense
}
