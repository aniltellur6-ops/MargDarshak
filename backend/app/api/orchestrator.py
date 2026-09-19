from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from app.orchestrator.workflow import margdarshak_app

router = APIRouter()

class OrchestratorRequest(BaseModel):
    raw_profile_text: str
    raw_job_text: str

@router.post("/run")
async def run_orchestrator_endpoint(req: OrchestratorRequest):
    try:
        initial_state = {
            "raw_profile_text": req.raw_profile_text,
            "raw_job_text": req.raw_job_text,
            "profile": None,
            "job": None,
            "gaps": None,
            "priorities": None
        }
        
        final_state = margdarshak_app.invoke(initial_state)
        
        # We need to serialize the output. FastAPI handles Pydantic natively if we return dict,
        # but the LangGraph state is a TypedDict. Let's return it directly.
        return final_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestrator failed: {str(e)}")
