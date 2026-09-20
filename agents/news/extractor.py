import os
import sys
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.schemas.news import NewsSignalCreate
from app.ontology.skill_graph import SkillGraphManager

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List

class NewsExtractionSchema(BaseModel):
    title: str
    summary: str
    impact_score: int = Field(description="1-10 scale indicating how much this news affects the job market", ge=1, le=10)
    raw_skills: List[str] = Field(description="List of raw technical skills, tools, or concepts explicitly impacted by this news")

def extract_news_signal(raw_text: str) -> NewsSignalCreate:
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
    structured_llm = llm.with_structured_output(NewsExtractionSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert tech industry analyst. Read the following news article. Extract a concise title, a technical summary, estimate the market impact score (1-10), and extract all specific technical skills or tools that are impacted (positively or negatively) by this news."),
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
    
    return NewsSignalCreate(
        signal_id=f"news_{uuid.uuid4().hex[:8]}",
        title=result.title,
        summary=result.summary,
        impact_score=result.impact_score,
        impacted_skills=canonical_skills
    )
