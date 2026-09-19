from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.assessment.generator import generate_assessment
from app.schemas.assessment import AssessmentQuiz

router = APIRouter()

class AssessmentRequest(BaseModel):
    skill_id: str
    difficulty: str = "Intermediate"

@router.post("/generate", response_model=AssessmentQuiz)
async def generate_assessment_endpoint(req: AssessmentRequest):
    try:
        quiz = generate_assessment(req.skill_id, req.difficulty)
        return quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment Generation failed: {str(e)}")
