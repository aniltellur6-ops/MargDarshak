import sys
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.profile.extractor import extract_profile, ProfileExtractionResult
from app.services.document_parser import parse_document

router = APIRouter()

@router.post("/extract", response_model=ProfileExtractionResult)
async def extract_profile_endpoint(
    text_input: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    raw_text = ""
    
    if file:
        file_bytes = await file.read()
        try:
            raw_text = parse_document(file_bytes, file.filename)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif text_input:
        raw_text = text_input
    else:
        raise HTTPException(status_code=400, detail="Must provide either text_input or file.")
        
    try:
        # Note: In a real app this might be an async call depending on the LLM library usage.
        # LangChain's sync invoke will block, so consider using ainvoke in production.
        profile = extract_profile(raw_text)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

