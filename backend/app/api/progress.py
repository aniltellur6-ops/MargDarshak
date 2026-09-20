from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.progress.tracker import update_progress
from app.schemas.profile import SkillEvidence
from agents.profile.extractor import ProfileExtractionResult
from app.schemas.job import JobCreate
from app.schemas.progress import ProgressUpdateReport

router = APIRouter()

class ProgressUpdateRequest(BaseModel):
    profile: ProfileExtractionResult
    new_evidence: SkillEvidence
    target_job: Optional[JobCreate] = None

@router.post("/update", response_model=ProgressUpdateReport)
async def update_progress_endpoint(req: ProgressUpdateRequest):
    try:
        report = update_progress(req.profile, req.new_evidence, req.target_job)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Progress Update failed: {str(e)}")
