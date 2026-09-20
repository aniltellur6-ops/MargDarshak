import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.engine.matching import MatchResult
from app.schemas.gap import GapReport, MissingSkill
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def analyze_gaps(match_result: MatchResult) -> GapReport:
    # 1. Deterministic Gap Filtering
    missing = []
    missing_skill_names_for_llm = []
    
    for detail in match_result.details:
        if detail.similarity_score < 1.0:
            missing.append(MissingSkill(
                skill_id=detail.requirement_skill_id,
                current_similarity_score=detail.similarity_score,
                is_mandatory=(detail.importance_weight == 1.0)
            ))
            missing_skill_names_for_llm.append(detail.requirement_skill_id)
            
    # 2. LLM Summary Generation
    if not missing_skill_names_for_llm:
        summary_text = "You are a perfect match for this role. No critical skill gaps identified."
    else:
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a career advisor. The user has matched {match_score}% with a job, but they are missing the following skills: {skills}. Write exactly two sentences summarizing their skill gap and advising them on what to focus on."),
            ])
            chain = prompt | llm
            response = chain.invoke({
                "match_score": match_result.overall_match_percentage,
                "skills": ", ".join(missing_skill_names_for_llm)
            })
            summary_text = response.content
        except Exception as e:
            # Fallback if LLM fails (e.g., API key missing in test)
            summary_text = f"You are missing the following skills: {', '.join(missing_skill_names_for_llm)}"
            
    return GapReport(
        job_id=match_result.job_id,
        overall_match_percentage=match_result.overall_match_percentage,
        summary=summary_text,
        missing_skills=missing
    )
