import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from agents.opportunity.unlocker import simulate_opportunity
from agents.profile.extractor import ProfileExtractionResult
from backend.app.schemas.profile import SkillEvidence
from backend.app.schemas.job import JobCreate, JobRequirementCreate
from backend.app.schemas.priority import PrioritizedGapReport, PrioritizedSkill

load_dotenv()

def run_test():
    # 1. Mock Profile (Only knows SQL)
    profile = ProfileExtractionResult(
        user_id="student_1",
        evidences=[
            SkillEvidence(skill_name="MySQL", evidence_type="course", evidence_description="Database class")
        ]
    )
    
    # 2. Mock Job (Needs SQL, Java, Docker)
    job = JobCreate(
        job_id="job_123",
        title="Backend Dev",
        company="TechCorp",
        location="Remote",
        description="Requires Java",
        requirements=[
            JobRequirementCreate(skill_id="JAVA", importance_score=1.0, is_mandatory=True),
            JobRequirementCreate(skill_id="DOCKER", importance_score=0.5, is_mandatory=False),
            JobRequirementCreate(skill_id="SQL", importance_score=1.0, is_mandatory=True)
        ]
    )
    
    # 3. Mock Prioritized Gap (Missing Java and Docker)
    gaps = PrioritizedGapReport(
        job_id="job_123",
        overall_match_percentage=40.0,  # Only SQL matched
        summary="Missing skills.",
        prioritized_skills=[
            PrioritizedSkill(skill_id="JAVA", current_similarity_score=0.0, is_mandatory=True, dependency_weight=5, priority_score=150.0, reason="important"),
            PrioritizedSkill(skill_id="DOCKER", current_similarity_score=0.0, is_mandatory=False, dependency_weight=0, priority_score=50.0, reason="terminal")
        ]
    )
    
    print("Running Opportunity Simulation (Learning Top 1 skill - JAVA)...")
    report = simulate_opportunity(profile, job, gaps, top_n=1)
    
    print("\nOpportunity Report:")
    print(report.model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
