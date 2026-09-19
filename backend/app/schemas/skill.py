from pydantic import BaseModel
from typing import List, Optional

class SkillBase(BaseModel):
    skill_id: str
    name: str
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    parent_id: Optional[int] = None
    
    class Config:
        from_attributes = True
