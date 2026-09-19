from pydantic import BaseModel
from typing import List, Optional

class CourseBase(BaseModel):
    provider: str
    title: str
    price: Optional[float] = None
    is_free: bool = False
    duration_hours: Optional[float] = None

class Course(CourseBase):
    id: int
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    difficulty: str
    expected_output: str

class Project(ProjectBase):
    id: int
    class Config:
        from_attributes = True

class AssessmentBase(BaseModel):
    skill_name: str
    score: float

class Assessment(AssessmentBase):
    id: int
    class Config:
        from_attributes = True
