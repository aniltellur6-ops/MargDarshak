from typing import TypedDict, Optional, List
from app.schemas.profile import ProfileExtractionResult
from app.schemas.job import JobCreate
from app.schemas.gap import GapAnalysisResult
from app.schemas.priority import PriorityScore

class MargDarshakState(TypedDict):
    raw_profile_text: str
    raw_job_text: str
    
    profile: Optional[ProfileExtractionResult]
    job: Optional[JobCreate]
    gaps: Optional[GapAnalysisResult]
    priorities: Optional[List[PriorityScore]]
