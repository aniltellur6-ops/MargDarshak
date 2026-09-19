import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.schemas.course import CourseCreate
from app.ontology.skill_graph import SkillGraphManager

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
import uuid

class CourseExtractionSchema(BaseModel):
    provider: str
    title: str
    description: str
    raw_skills: List[str] = Field(description="List of skills, tools, or concepts taught in this course")

def extract_course(raw_text: str) -> CourseCreate:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = llm.with_structured_output(CourseExtractionSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert curriculum analyzer. Extract the course provider, title, description, and every distinct technical skill or concept taught in the text."),
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
    
    return CourseCreate(
        course_id=f"course_{uuid.uuid4().hex[:8]}",
        provider=result.provider,
        title=result.title,
        description=result.description,
        url="https://example.com/course",
        skills_taught=canonical_skills
    )
