from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class GlobalConfig(Base):
    __tablename__ = "global_config"
    
    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[float] = mapped_column(Float, default=1.0)
