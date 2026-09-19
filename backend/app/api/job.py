from fastapi import APIRouter, HTTPException, Body
from app.schemas.job import JobCreate
from app.ontology.skill_graph import SkillGraphManager
from app.services.job_service import parse_and_normalize_job

router = APIRouter()

@router.post("/extract", response_model=JobCreate)
async def extract_job_endpoint(
    text_input: str = Body(..., embed=True, description="Raw job description text")
):
    try:
        job = parse_and_normalize_job(text_input)
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job Extraction failed: {str(e)}")

