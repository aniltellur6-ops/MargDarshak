from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.project.extractor import extract_project
from app.schemas.project import ProjectCreate

router = APIRouter()

class ProjectExtractionRequest(BaseModel):
    raw_text: str

@router.post("/extract", response_model=ProjectCreate)
async def extract_project_endpoint(req: ProjectExtractionRequest):
    try:
        project = extract_project(req.raw_text)
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Project Extraction failed: {str(e)}")
