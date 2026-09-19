import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.schemas.gap import GapReport
from app.schemas.priority import PrioritizedGapReport, PrioritizedSkill
from app.ontology.skill_graph import SkillGraphManager

def prioritize_gaps(report: GapReport) -> PrioritizedGapReport:
    manager = SkillGraphManager()
    
    prioritized_list = []
    
    for missing in report.missing_skills:
        # Calculate Base Score
        base_score = 100.0 if missing.is_mandatory else 50.0
        
        # Calculate Graph Centrality Score
        deps = manager.get_skill_dependency_weight(missing.skill_id)
        graph_bonus = deps * 10.0
        
        total_score = base_score + graph_bonus
        
        # Generate Reason string
        req_str = "Must-have requirement." if missing.is_mandatory else "Nice-to-have requirement."
        if deps > 0:
            reason = f"{req_str} Foundational skill unlocking {deps} other concepts in the ontology."
        else:
            reason = f"{req_str} Terminal skill with no strict downstream dependencies."
            
        prioritized_list.append(PrioritizedSkill(
            skill_id=missing.skill_id,
            current_similarity_score=missing.current_similarity_score,
            is_mandatory=missing.is_mandatory,
            dependency_weight=deps,
            priority_score=total_score,
            reason=reason
        ))
        
    manager.close()
    
    # Sort descending by priority_score
    prioritized_list.sort(key=lambda x: x.priority_score, reverse=True)
    
    return PrioritizedGapReport(
        job_id=report.job_id,
        overall_match_percentage=report.overall_match_percentage,
        summary=report.summary,
        prioritized_skills=prioritized_list
    )
