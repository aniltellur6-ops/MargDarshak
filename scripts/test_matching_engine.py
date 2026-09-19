import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from backend.app.engine.matching import match_profile_to_job
from agents.profile.extractor import ProfileExtractionResult
from backend.app.schemas.profile import SkillEvidence
from backend.app.schemas.job import JobCreate, JobRequirementCreate

def run_test():
    # Mock a student profile (Knows Java and SQL)
    profile = ProfileExtractionResult(
        user_id="student_1",
        evidences=[
            SkillEvidence(skill_name="Core Java", evidence_type="project", evidence_description="Built app"),
            SkillEvidence(skill_name="MySQL", evidence_type="course", evidence_description="Database class")
        ]
    )
    
    # Mock a Job (Wants Spring Boot and Docker)
    job = JobCreate(
        job_id="job_123",
        title="Backend Dev",
        company="TechCorp",
        location="Remote",
        description="Requires Spring Boot",
        requirements=[
            JobRequirementCreate(skill_id="SPRING_BOOT", importance_score=1.0, is_mandatory=True),
            JobRequirementCreate(skill_id="DOCKER", importance_score=0.5, is_mandatory=False),
            JobRequirementCreate(skill_id="SQL", importance_score=1.0, is_mandatory=True)
        ]
    )
    
    print("Calculating deterministic match...")
    result = match_profile_to_job(profile, job)
    
    print(f"\nOverall Match Score: {result.overall_match_percentage}%")
    print("\nDetailed breakdown:")
    for d in result.details:
        print(f"- Req: {d.requirement_skill_id} | Best Match: {d.best_match_skill_id} | Sim Score: {d.similarity_score} | Earned: {d.weighted_score}/{d.importance_weight}")

if __name__ == "__main__":
    run_test()
