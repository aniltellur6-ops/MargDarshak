from typing import List, Dict, Any
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.profile.extractor import ProfileExtractionResult
from agents.job.extractor import JobExtractionResult
from app.ontology.skill_graph import SkillGraphManager

class SkillMatchDetail(BaseModel):
    requirement_skill_id: str
    best_match_skill_id: str
    similarity_score: float
    importance_weight: float
    weighted_score: float

class MatchResult(BaseModel):
    job_id: str
    overall_match_percentage: float
    details: List[SkillMatchDetail]

def match_profile_to_job(profile: ProfileExtractionResult, job: JobExtractionResult) -> MatchResult:
    manager = SkillGraphManager()
    
    # Normalize student profile skills
    student_canonical_skills = []
    for evidence in profile.evidences:
        canonical_id = manager.normalize_skill(evidence.skill_name)
        if canonical_id:
            student_canonical_skills.append(canonical_id)
        else:
            student_canonical_skills.append(evidence.skill_name.upper().replace(' ', '_'))
            
    # De-duplicate
    student_canonical_skills = list(set(student_canonical_skills))
    
    match_details = []
    total_possible_weight = 0.0
    total_earned_weight = 0.0
    
    # Process Must Have Skills
    for skill_name in job.must_have_skills:
        req_id = manager.normalize_skill(skill_name) or skill_name.upper().replace(' ', '_')
        weight = 1.0
        total_possible_weight += weight
        
        best_score = 0.0
        best_match_id = "NONE"
        
        for student_skill in student_canonical_skills:
            score = manager.calculate_similarity(req_id, student_skill)
            if score > best_score:
                best_score = score
                best_match_id = student_skill
                
        earned = best_score * weight
        total_earned_weight += earned
        
        match_details.append(SkillMatchDetail(
            requirement_skill_id=req_id,
            best_match_skill_id=best_match_id,
            similarity_score=best_score,
            importance_weight=weight,
            weighted_score=earned
        ))

    # Process Nice To Have Skills
    for skill_name in job.nice_to_have_skills:
        req_id = manager.normalize_skill(skill_name) or skill_name.upper().replace(' ', '_')
        weight = 0.5
        total_possible_weight += weight
        
        best_score = 0.0
        best_match_id = "NONE"
        
        for student_skill in student_canonical_skills:
            score = manager.calculate_similarity(req_id, student_skill)
            if score > best_score:
                best_score = score
                best_match_id = student_skill
                
        earned = best_score * weight
        total_earned_weight += earned
        
        match_details.append(SkillMatchDetail(
            requirement_skill_id=req_id,
            best_match_skill_id=best_match_id,
            similarity_score=best_score,
            importance_weight=weight,
            weighted_score=earned
        ))
        
    manager.close()
    
    percentage = (total_earned_weight / total_possible_weight) * 100 if total_possible_weight > 0 else 0.0
    
    return MatchResult(
        job_id=job.title,
        overall_match_percentage=round(percentage, 2),
        details=match_details
    )
