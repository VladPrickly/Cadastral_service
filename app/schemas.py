from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class QueryRequest(BaseModel):
    cadastral_number: str = Field(..., description="Кадастровый номер")
    latitude: float = Field(..., description="Широта")
    longitude: float = Field(..., description="Долгота")


class QueryResponse(BaseModel):
    id: int
    cadastral_number: str
    latitude: float
    longitude: float
    result: Optional[bool]
    created_at: datetime

    class Config:
        from_attributes = True