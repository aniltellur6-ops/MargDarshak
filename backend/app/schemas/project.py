from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectCreate(BaseModel):
    project_id: str
    title: str
    description: str
    difficulty_level: str = Field(description="e.g., Beginner, Intermediate, Advanced")
    url: Optional[str] = None
    skills_validated: List[str] = Field(description="List of canonical skill IDs from our ontology proven by this project")
