import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from agents.gap.prioritizer import prioritize_gaps
from backend.app.schemas.gap import GapReport, MissingSkill

load_dotenv()

def run_test():
    # Mock a GapReport from Phase 5
    # JAVA has dependencies in our taxonomy. DOCKER does not have children.
    mock_report = GapReport(
        job_id="job_789",
        overall_match_percentage=40.0,
        summary="You need to learn Java and Docker.",
        missing_skills=[
            MissingSkill(skill_id="DOCKER", current_similarity_score=0.0, is_mandatory=True),
            MissingSkill(skill_id="JAVA", current_similarity_score=0.0, is_mandatory=True)
        ]
    )
    
    print("Running Gap Prioritization...")
    prioritized = prioritize_gaps(mock_report)
    
    print("\nPrioritized Gap Report Result:")
    print(prioritized.model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
