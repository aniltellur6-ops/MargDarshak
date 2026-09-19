from pydantic import BaseModel
from typing import Optional

class CareerNewsBase(BaseModel):
    title: str
    source: str
    summary: str
    relevance_reason: str

class CareerNews(CareerNewsBase):
    id: int
    class Config:
        from_attributes = True
