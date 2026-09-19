from fastapi import APIRouter, HTTPException, Body
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.gap.prioritizer import prioritize_gaps
from app.schemas.gap import GapReport
from app.schemas.priority import PrioritizedGapReport

router = APIRouter()

@router.post("/prioritize", response_model=PrioritizedGapReport)
async def prioritize_gap_endpoint(
    report: GapReport = Body(...)
):
    try:
        prioritized = prioritize_gaps(report)
        return prioritized
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gap Prioritization failed: {str(e)}")
