from pydantic import BaseModel
from typing import List, Optional

class ProgressBase(BaseModel):
    user_id: str
    backend_readiness: float = 0.0
    matching_jobs_count: int = 0

class Recommendation(BaseModel):
    type: str # course, project, skill
    item_id: str
    reason: str

class Progress(ProgressBase):
    id: int
    class Config:
        from_attributes = True
