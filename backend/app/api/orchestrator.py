from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from app.orchestrator.workflow import margdarshak_app
from app.services.document_parser import parse_document

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
        return final_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestrator failed: {str(e)}")

@router.post("/analyze")
async def analyze_profile_endpoint(
    resume_file: UploadFile = File(...),
    job_description: Optional[str] = Form("")
):
    try:
        file_bytes = await resume_file.read()
        raw_profile_text = parse_document(file_bytes, resume_file.filename)
        
        initial_state = {
            "raw_profile_text": raw_profile_text,
            "raw_job_text": job_description or "",
            "profile": None,
            "job": None,
            "gaps": None,
            "priorities": None
        }
        
        final_state = margdarshak_app.invoke(initial_state)
        return final_state
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Orchestrator analysis failed: {str(e)}")
