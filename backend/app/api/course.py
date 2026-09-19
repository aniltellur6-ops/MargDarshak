from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.course.extractor import extract_course
from app.schemas.course import CourseCreate

router = APIRouter()

class CourseExtractionRequest(BaseModel):
    raw_text: str

@router.post("/extract", response_model=CourseCreate)
async def extract_course_endpoint(req: CourseExtractionRequest):
    try:
        course = extract_course(req.raw_text)
        return course
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Course Extraction failed: {str(e)}")
