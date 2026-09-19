import os
import sys
from typing import Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.schemas.profile import ProfileExtractionResult, SkillEvidence
from app.schemas.job import JobCreate
from app.schemas.progress import ProgressUpdateReport
from app.engine.matching import match_profile_to_job
from app.ontology.skill_graph import SkillGraphManager

def update_progress(
    profile: ProfileExtractionResult,
    new_evidence: SkillEvidence,
    target_job: Optional[JobCreate] = None
) -> ProgressUpdateReport:
    
    manager = SkillGraphManager()
    
    # 1. Normalize the new skill to ensure we are using canonical IDs
    canonical_new_skill = manager.normalize_skill(new_evidence.skill_name)
    if not canonical_new_skill:
        canonical_new_skill = new_evidence.skill_name.upper()
    
    new_evidence.skill_name = canonical_new_skill
    
    # 2. Check if the skill already exists in the profile
    was_added = False
    existing_skills = [ev.skill_name for ev in profile.evidences]
    
    if canonical_new_skill not in existing_skills:
        profile.evidences.append(new_evidence)
        was_added = True
        
    manager.close()
    
    # 3. Recalculate match score if a target job is provided
    new_match_result = None
    if target_job:
        new_match_result = match_profile_to_job(profile, target_job)
        
    return ProgressUpdateReport(
        updated_profile=profile,
        was_skill_added=was_added,
        new_match_result=new_match_result
    )
