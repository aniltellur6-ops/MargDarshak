import os
import sys
import json
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from agents.progress.tracker import update_progress
from backend.app.schemas.profile import ProfileExtractionResult, SkillEvidence
from backend.app.schemas.job import JobCreate

load_dotenv()

def run_test():
    # 1. Setup Initial Profile (Knows Python, but not Kubernetes)
    profile = ProfileExtractionResult(
        first_name="Alice",
        last_name="Smith",
        current_role="Junior Developer",
        years_of_experience=1,
        evidences=[
            SkillEvidence(skill_name="PYTHON", proficiency="Intermediate", context="Work")
        ]
    )
    
    # 2. Setup Target Job (Requires Python AND Kubernetes)
    job = JobCreate(
        job_id="job_456",
        title="Backend Engineer",
        company="TechCorp",
        description="Need a backend engineer",
        skills_required=["PYTHON", "KUBERNETES"]
    )
    
    # 3. Simulate passing an assessment for Kubernetes
    new_evidence = SkillEvidence(
        skill_name="KUBERNETES",
        proficiency="Intermediate",
        context="Passed MargDarshak Assessment QZ-999"
    )
    
    print("--- Before Update ---")
    print(f"Profile Skills: {[e.skill_name for e in profile.evidences]}")
    
    print("\n--- Running Progress Engine ---")
    report = update_progress(profile, new_evidence, target_job=job)
    
    print("\n--- After Update ---")
    print(f"Skill Added: {report.was_skill_added}")
    print(f"Updated Profile Skills: {[e.skill_name for e in report.updated_profile.evidences]}")
    if report.new_match_result:
        print(f"New Match Score against Target Job: {report.new_match_result.overall_match_score * 100:.2f}%")

if __name__ == "__main__":
    run_test()
