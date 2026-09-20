import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from langgraph.graph import StateGraph, START, END

from app.orchestrator.state import MargDarshakState
from agents.profile.extractor import extract_profile
from agents.job.extractor import extract_job
from agents.gap.analyzer import analyze_gaps
from agents.gap.prioritizer import prioritize_gaps

def node_extract_profile(state: MargDarshakState) -> MargDarshakState:
    profile = extract_profile(state["raw_profile_text"])
    return {"profile": profile}

def node_extract_job(state: MargDarshakState) -> MargDarshakState:
    job = extract_job(state["raw_job_text"])
    return {"job": job}

from app.engine.matching import match_profile_to_job

def node_analyze_gaps(state: MargDarshakState) -> MargDarshakState:
    match_result = match_profile_to_job(state["profile"], state["job"])
    gaps = analyze_gaps(match_result)
    return {"gaps": gaps}
def node_prioritize_gaps(state: MargDarshakState) -> MargDarshakState:
    priorities = prioritize_gaps(state["gaps"])
    return {"priorities": priorities}

# Build the Graph
workflow = StateGraph(MargDarshakState)

workflow.add_node("extract_profile", node_extract_profile)
workflow.add_node("extract_job", node_extract_job)
workflow.add_node("analyze_gaps", node_analyze_gaps)
workflow.add_node("prioritize_gaps", node_prioritize_gaps)

workflow.add_edge(START, "extract_profile")
workflow.add_edge("extract_profile", "extract_job")
workflow.add_edge("extract_job", "analyze_gaps")
workflow.add_edge("analyze_gaps", "prioritize_gaps")
workflow.add_edge("prioritize_gaps", END)

margdarshak_app = workflow.compile()
