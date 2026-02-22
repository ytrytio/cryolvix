from sqlalchemy import BigInteger, String, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from typing import List
from .base import Base
from .gpu import GPU


class User(Base):
    from cryolvix.core.license import License
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    created: Mapped[int] = mapped_column(BigInteger, nullable=False)
    
    money: Mapped[Decimal] = mapped_column(Numeric(precision=38, scale=2), default=0)
    cryocoins: Mapped[Decimal] = mapped_column(Numeric(precision=38, scale=2), default=0)

    gpus: Mapped[List["GPU"]] = relationship("GPU", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    
    cooldown: Mapped[int] = mapped_column(BigInteger, default=0, nullable=True)
    _license: Mapped[int] = mapped_column("license", Integer, default=0, nullable=True)
    subscription: Mapped[int] = mapped_column(BigInteger, default=0, nullable=True)
    
    @property
    def license(self) -> License:
        from cryolvix.core.license import NoLicense, LICENSES
        return LICENSES.get(self._license, NoLicense)
