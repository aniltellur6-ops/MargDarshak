from pydantic import BaseModel
from typing import List, Optional

class JobBase(BaseModel):
    job_id: str
    role: str
    company: str
    location: Optional[str] = None

class JobRequirement(BaseModel):
    skill_name: str
    is_required: bool = True

class JobCreate(JobBase):
    requirements: List[JobRequirement] = []

class Job(JobBase):
    id: int
    requirements: List[JobRequirement] = []
    
    class Config:
        from_attributes = True
