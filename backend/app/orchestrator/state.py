from typing import TypedDict, Optional, List
from agents.profile.extractor import ProfileExtractionResult
from app.schemas.job import JobCreate
from app.schemas.gap import GapReport
from app.schemas.priority import PrioritizedSkill

class MargDarshakState(TypedDict):
    raw_profile_text: str
    raw_job_text: str
    
    profile: Optional[ProfileExtractionResult]
    job: Optional[JobCreate]
    gaps: Optional[GapReport]
    priorities: Optional[List[PrioritizedSkill]]
