from pydantic import BaseModel
from typing import List

class OpportunityUnlockReport(BaseModel):
    job_id: str
    original_score: float
    projected_score: float
    score_increase: float
    skills_simulated: List[str]
    motivation_summary: str
