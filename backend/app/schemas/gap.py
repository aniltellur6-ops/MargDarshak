from pydantic import BaseModel, Field
from typing import List

class MissingSkill(BaseModel):
    skill_id: str
    current_similarity_score: float
    is_mandatory: bool = Field(description="True if this was a must-have requirement")

class GapReport(BaseModel):
    job_id: str
    overall_match_percentage: float
    summary: str = Field(description="LLM-generated high-level summary of the gaps")
    missing_skills: List[MissingSkill]
