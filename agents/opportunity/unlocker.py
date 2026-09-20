import os
import sys
import copy

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from agents.profile.extractor import ProfileExtractionResult
from app.schemas.profile import SkillEvidence
from app.schemas.job import JobCreate
from app.schemas.priority import PrioritizedGapReport
from app.schemas.opportunity import OpportunityUnlockReport
from app.engine.matching import match_profile_to_job

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def simulate_opportunity(
    profile: ProfileExtractionResult, 
    job: JobCreate, 
    prioritized_gaps: PrioritizedGapReport, 
    top_n: int = 2
) -> OpportunityUnlockReport:
    
    original_score = prioritized_gaps.overall_match_percentage
    
    # 1. Extract top N skills to simulate
    skills_to_simulate = []
    for i, skill in enumerate(prioritized_gaps.prioritized_skills):
        if i < top_n:
            skills_to_simulate.append(skill.skill_id)
            
    if not skills_to_simulate:
        return OpportunityUnlockReport(
            job_id=job.job_id,
            original_score=original_score,
            projected_score=original_score,
            score_increase=0.0,
            skills_simulated=[],
            motivation_summary="You already have all the required skills for this role!"
        )
            
    # 2. Deep copy profile and inject simulated evidence
    simulated_profile = copy.deepcopy(profile)
    for skill_id in skills_to_simulate:
        simulated_profile.evidences.append(
            SkillEvidence(
                skill_name=skill_id, 
                evidence_type="simulated", 
                evidence_description="Simulated learning completion"
            )
        )
        
    # 3. Recalculate match
    new_match_result = match_profile_to_job(simulated_profile, job)
    projected_score = new_match_result.overall_match_percentage
    score_increase = round(projected_score - original_score, 2)
    
    # 4. Generate LLM motivation
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a highly motivating career coach. If the student learns {skills}, their match for the job jumps from {old_score}% to {new_score}%. Write exactly one punchy, highly encouraging sentence to motivate them to start learning these skills immediately.")
        ])
        chain = prompt | llm
        response = chain.invoke({
            "skills": ", ".join(skills_to_simulate),
            "old_score": original_score,
            "new_score": projected_score
        })
        motivation = response.content
    except Exception as e:
        motivation = f"By learning {', '.join(skills_to_simulate)}, your match score will jump by {score_increase}%!"
        
    return OpportunityUnlockReport(
        job_id=job.job_id,
        original_score=original_score,
        projected_score=projected_score,
        score_increase=score_increase,
        skills_simulated=skills_to_simulate,
        motivation_summary=motivation
    )
