from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.opportunity.unlocker import simulate_opportunity
from agents.profile.extractor import ProfileExtractionResult
from app.schemas.job import JobCreate
from app.schemas.priority import PrioritizedGapReport
from app.schemas.opportunity import OpportunityUnlockReport

router = APIRouter()

class OpportunityRequest(BaseModel):
    profile: ProfileExtractionResult
    job: JobCreate
    prioritized_gaps: PrioritizedGapReport
    top_n: int = 2

@router.post("/simulate", response_model=OpportunityUnlockReport)
async def simulate_opportunity_endpoint(req: OpportunityRequest):
    try:
        report = simulate_opportunity(req.profile, req.job, req.prioritized_gaps, req.top_n)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Opportunity Simulation failed: {str(e)}")
