from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from .db import Base


class CadastralQuery(Base):
    __tablename__ = "cadastral_queries"

    id = Column(Integer, primary_key=True, index=True)
    cadastral_number = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    result = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())