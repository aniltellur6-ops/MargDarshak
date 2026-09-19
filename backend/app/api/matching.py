from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.engine.matching import match_profile_to_job, MatchResult
from app.schemas.job import JobCreate
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.profile.extractor import ProfileExtractionResult

router = APIRouter()

class MatchRequest(BaseModel):
    profile: ProfileExtractionResult
    job: JobCreate

@router.post("/calculate", response_model=MatchResult)
async def calculate_match(req: MatchRequest):
    try:
        result = match_profile_to_job(req.profile, req.job)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching calculation failed: {str(e)}")
