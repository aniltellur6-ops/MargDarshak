import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from backend.app.orchestrator.workflow import margdarshak_app

load_dotenv()

def run_test():
    raw_profile = "I am a backend developer. I know Python and Postgres very well."
    raw_job = "We need a Senior Backend Engineer. You must know Python, Postgres, and Kubernetes."
    
    print("Running MargDarshak Orchestrator End-to-End...")
    
    initial_state = {
        "raw_profile_text": raw_profile,
        "raw_job_text": raw_job,
        "profile": None,
        "job": None,
        "gaps": None,
        "priorities": None
    }
    
    final_state = margdarshak_app.invoke(initial_state)
    
    print("\n--- Final Prioritized Gaps ---")
    priorities = final_state.get("priorities", [])
    for idx, p in enumerate(priorities):
        print(f"{idx+1}. {p.skill_id} (Score: {p.priority_score:.2f})")
        print(f"   Reason: {p.reason}")

if __name__ == "__main__":
    run_test()
