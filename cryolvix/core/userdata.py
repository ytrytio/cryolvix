from aiogram.types import User as TelegramUser
from html import escape as html_escape
from typing import Optional
from datetime import datetime
from decimal import Decimal
from time import time as unixtime

from cryolvix.config import SUBSCRIPTION_TIME
from cryolvix.core.license import License, NoLicense, LICENSES
from cryolvix.database.repositories.user_repo import UserRepository
from cryolvix.database.models.user import User as UserModel

class UserData:
    def __init__(
        self, 
        user_id: int, 
        name: str, 
        username: Optional[str] = None, 
        money: float = 0.0, 
        cryocoins: float = 0.0, 
        created: Optional[int] = None,
        cooldown: int = 0,
        _license: int = 0,
        subscription: int = 0,
        gpus: Optional[list] = None
    ):
        self.id = user_id
        self.name = name
        self.username = username.lower() if username else None
        self.money = money
        self.cryocoins = cryocoins
        self.created = created or int(datetime.now().timestamp())
        self.cooldown = cooldown or 0
        self._license = _license
        self.subscription: int = subscription or 0
        self.gpus = gpus or []

    @classmethod
    def from_model(cls, model: UserModel) -> "UserData":
        return cls(
            user_id=model.id,
            name=model.name,
            username=model.username,
            money=float(model.money),
            cryocoins=float(model.cryocoins),
            created=model.created,
            cooldown=model.cooldown,
            _license=model._license,
            subscription=model.subscription,
            gpus=model.gpus
        )
        
    @property
    def hashrate(self) -> float:
        return sum(gpu.multiplier for gpu in self.gpus)

    @classmethod
    async def create_or_load(cls, user: TelegramUser, repo: UserRepository) -> "UserData":
        safe_name = html_escape(user.first_name)
        db_user = await repo.get_or_create(
            user_id=user.id,
            name=safe_name,
            username=user.username
        )
        return cls.from_model(db_user)

    async def update(self, repo: UserRepository):
        await repo.update(
            user_id=self.id,
            name=self.name,
            username=self.username,
            money=Decimal(str(self.money)),
            cryocoins=Decimal(str(self.cryocoins)),
            cooldown=self.cooldown,
            _license=self._license,
            subscription=self.subscription
        )
        
    @property
    def license(self):
        return LICENSES.get(self._license, NoLicense)

    @license.setter
    def license(self, license_obj: License):
        uid = next((k for k, v in LICENSES.items() if v == license_obj), 0)
        now = int(unixtime())
        self._license = uid
        self.subscription = (now + SUBSCRIPTION_TIME) if uid > 0 else 0
            
    async def check_license(self) -> int:
        now = int(unixtime())
        if self.subscription < now:
            self.license = NoLicense
        else:
            return self.subscription - now
        return 0

    @property
    def link(self) -> str:
        if self.username:
            return f'<a href="https://t.me/{self.username}">{self.name}</a>'
        return f'<a href="tg://user?id={self.id}">{self.name}</a>'
