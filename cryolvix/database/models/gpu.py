from sqlalchemy import Column, BigInteger, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class GPU(Base):
    __tablename__ = "gpus"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created = Column(BigInteger, nullable=False)
    
    company = Column(String, nullable=False)
    # model = Column(String, nullable=False)
    prefix = Column(String, nullable=False)
    series = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    suffix = Column(String, nullable=False)
    
    working = Column(Boolean, default=True)
    temperature = Column(Integer, default=60)

    multiplier = Column(Integer, default=1)
    wearout = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="gpus")
