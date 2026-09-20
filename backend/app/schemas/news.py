from pydantic import BaseModel, Field
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

from typing import List

class NewsSignalCreate(BaseModel):
    signal_id: str
    title: str
    summary: str
    impact_score: int = Field(description="1-10 scale indicating how much this news affects the job market", ge=1, le=10)
    impacted_skills: List[str] = Field(description="List of canonical skill IDs impacted by this news")
