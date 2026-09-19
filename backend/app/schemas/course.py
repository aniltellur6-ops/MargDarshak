from pydantic import BaseModel, Field
from typing import List, Optional

class CourseCreate(BaseModel):
    course_id: str
    provider: str = Field(description="e.g., Udemy, Coursera")
    title: str
    description: str
    url: Optional[str] = None
    skills_taught: List[str] = Field(description="List of canonical skill IDs from our ontology")
