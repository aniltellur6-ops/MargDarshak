import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.job.extractor import extract_job, JobExtractionResult
from app.schemas.job import JobCreate, JobRequirement
from app.ontology.skill_graph import SkillGraphManager
import uuid

def parse_and_normalize_job(raw_text: str) -> JobCreate:
    # 1. Extract raw job data using LLM
    extracted: JobExtractionResult = extract_job(raw_text)
    
    # 2. Normalize skills against Ontology
    manager = SkillGraphManager()
    
    requirements = []
    
    # Helper to map skills
    def map_skills(skill_list, weight):
        for raw_skill in skill_list:
            canonical_id = manager.normalize_skill(raw_skill)
            # If we don't find it in ontology, we just use the raw name in uppercase as a fallback
            skill_id_to_use = canonical_id if canonical_id else raw_skill.upper().replace(' ', '_')
            
            req = JobRequirement(
                skill_name=skill_id_to_use,
                is_required=(weight == 1.0)
            )
            requirements.append(req)
            
    # Map must haves (weight 1.0)
    map_skills(extracted.must_have_skills, 1.0)
    
    # Map nice to haves (weight 0.5)
    map_skills(extracted.nice_to_have_skills, 0.5)
    
    manager.close()
    
    # 3. Construct canonical Job Schema
    # generate a random job id for MVP
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    
    job = JobCreate(
        job_id=job_id,
        role=extracted.title,
        company=extracted.company,
        location=extracted.location or "Remote",
        requirements=requirements
    )
    
    return job
