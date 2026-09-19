import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from backend.app.ontology.skill_graph import SkillGraphManager
from backend.app.schemas.profile import ProfileExtractionResult, SkillEvidence
from backend.app.schemas.job import JobCreate

load_dotenv()

def run_test():
    manager = SkillGraphManager()
    
    # Ensure Skills exist
    manager.add_skill("PYTHON", "Programming Language", "Core Python")
    manager.add_skill("KUBERNETES", "Infrastructure", "Container Orchestration")
    manager.add_skill("DOCKER", "Infrastructure", "Containerization")
    
    print("Saving Profile to Neo4j...")
    profile = ProfileExtractionResult(
        first_name="Bob",
        last_name="Builder",
        current_role="DevOps Engineer",
        years_of_experience=3,
        evidences=[
            SkillEvidence(skill_name="DOCKER", proficiency="Advanced", context="Work"),
            SkillEvidence(skill_name="PYTHON", proficiency="Intermediate", context="School")
        ]
    )
    manager.save_profile("user_bob_123", profile)
    
    print("Saving Job to Neo4j...")
    job = JobCreate(
        job_id="job_k8s_admin",
        title="Kubernetes Administrator",
        company="CloudCo",
        description="We need K8s and Docker experts.",
        skills_required=["KUBERNETES", "DOCKER"]
    )
    manager.save_job(job)
    
    # Query Neo4j to verify
    with manager.driver.session() as session:
        print("\n--- Verifying Student Edges ---")
        student_rels = session.run("MATCH (s:Student {id: 'user_bob_123'})-[r:HAS_SKILL]->(sk:Skill) RETURN sk.skill_id as skill, r.proficiency as prof")
        for record in student_rels:
            print(f"Student HAS_SKILL: {record['skill']} (Proficiency: {record['prof']})")
            
        print("\n--- Verifying Job Edges ---")
        job_rels = session.run("MATCH (j:Job {id: 'job_k8s_admin'})-[r:REQUIRES_SKILL]->(sk:Skill) RETURN sk.skill_id as skill")
        for record in job_rels:
            print(f"Job REQUIRES_SKILL: {record['skill']}")

    manager.close()

if __name__ == "__main__":
    run_test()
