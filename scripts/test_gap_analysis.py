import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from agents.gap.analyzer import analyze_gaps
from backend.app.engine.matching import MatchResult, SkillMatchDetail

load_dotenv()

def run_test():
    # Mock a MatchResult from Phase 4
    mock_match = MatchResult(
        job_id="job_456",
        overall_match_percentage=66.6,
        details=[
            SkillMatchDetail(requirement_skill_id="JAVA", best_match_skill_id="JAVA", similarity_score=1.0, importance_weight=1.0, weighted_score=1.0),
            SkillMatchDetail(requirement_skill_id="SPRING_BOOT", best_match_skill_id="JAVA", similarity_score=0.8, importance_weight=1.0, weighted_score=0.8),
            SkillMatchDetail(requirement_skill_id="DOCKER", best_match_skill_id="NONE", similarity_score=0.0, importance_weight=1.0, weighted_score=0.0)
        ]
    )
    
    print("Running Gap Analysis...")
    report = analyze_gaps(mock_match)
    
    print("\nGap Report Result:")
    print(report.model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
