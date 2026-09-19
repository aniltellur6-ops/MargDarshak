from pydantic import BaseModel
from typing import List, Optional

class SkillEvidence(BaseModel):
    skill_name: str
    evidence: str
    evidence_type: str  # project, course, assessment, experience

class StudentProfileBase(BaseModel):
    user_id: str
    education_degree: Optional[str] = None
    education_branch: Optional[str] = None
    target_role: Optional[str] = None
    target_company: Optional[str] = None
    location: Optional[str] = None

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfile(StudentProfileBase):
    id: int
    evidences: List[SkillEvidence] = []
    
    class Config:
        from_attributes = True
