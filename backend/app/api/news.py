from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.news.extractor import extract_news_signal
from app.schemas.news import NewsSignalCreate

router = APIRouter()

class NewsExtractionRequest(BaseModel):
    raw_text: str

@router.post("/extract", response_model=NewsSignalCreate)
async def extract_news_endpoint(req: NewsExtractionRequest):
    try:
        signal = extract_news_signal(req.raw_text)
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News Extraction failed: {str(e)}")
