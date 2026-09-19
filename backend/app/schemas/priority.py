from pydantic import BaseModel, Field
from typing import List

class PrioritizedSkill(BaseModel):
    skill_id: str
    current_similarity_score: float
    is_mandatory: bool
    dependency_weight: int = Field(description="Number of other skills that depend on this one")
    priority_score: float = Field(description="Calculated ROI score (Base + Graph weight)")
    reason: str = Field(description="Explanation of the score")

class PrioritizedGapReport(BaseModel):
    job_id: str
    overall_match_percentage: float
    summary: str
    prioritized_skills: List[PrioritizedSkill]
