import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.schemas.project import ProjectCreate
from app.ontology.skill_graph import SkillGraphManager

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List
import uuid

class ProjectExtractionSchema(BaseModel):
    title: str
    description: str
    difficulty_level: str = Field(description="Must be exactly one of: Beginner, Intermediate, Advanced")
    raw_skills: List[str] = Field(description="List of skills, tools, frameworks, or concepts proven by building this project")

def extract_project(raw_text: str) -> ProjectCreate:
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
    structured_llm = llm.with_structured_output(ProjectExtractionSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert technical assessor. Analyze the project description. Extract the title, write a concise technical description, estimate the difficulty (Beginner, Intermediate, Advanced), and extract every distinct technical skill or concept that building this project proves the author knows."),
        ("user", "{text}")
    ])
    
    chain = prompt | structured_llm
    
    # 1. LLM Extraction
    result = chain.invoke({"text": raw_text})
    
    # 2. Ontology Normalization
    manager = SkillGraphManager()
    canonical_skills = []
    
    for raw_skill in result.raw_skills:
        canonical_id = manager.normalize_skill(raw_skill)
        if canonical_id:
            canonical_skills.append(canonical_id)
            
    manager.close()
    
    # Deduplicate
    canonical_skills = list(set(canonical_skills))
    
    return ProjectCreate(
        project_id=f"proj_{uuid.uuid4().hex[:8]}",
        title=result.title,
        description=result.description,
        difficulty_level=result.difficulty_level,
        url=None,
        skills_validated=canonical_skills
    )
