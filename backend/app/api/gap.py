from fastapi import APIRouter, HTTPException, Body
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.gap.analyzer import analyze_gaps
from app.schemas.gap import GapReport
from app.engine.matching import MatchResult

router = APIRouter()

@router.post("/analyze", response_model=GapReport)
async def analyze_gap_endpoint(
    match_result: MatchResult = Body(...)
):
    try:
        report = analyze_gaps(match_result)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gap Analysis failed: {str(e)}")
