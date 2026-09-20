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

from agents.profile.extractor import ProfileExtractionResult
from app.engine.matching import MatchResult

class ProgressUpdateReport(BaseModel):
    updated_profile: ProfileExtractionResult
    was_skill_added: bool
    new_match_result: Optional[MatchResult] = None
