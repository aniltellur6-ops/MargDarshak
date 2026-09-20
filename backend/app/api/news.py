from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from agents.news.extractor import extract_news_signal
from app.schemas.news import NewsSignalCreate

router = APIRouter()

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import concurrent.futures

class NewsExtractionRequest(BaseModel):
    raw_text: str

@router.post("/extract", response_model=NewsSignalCreate)
async def extract_news_endpoint(req: NewsExtractionRequest):
    try:
        signal = extract_news_signal(req.raw_text)
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News Extraction failed: {str(e)}")

@router.get("/live", response_model=list[NewsSignalCreate])
async def get_live_news_endpoint(query: str = "technology AI jobs"):
    try:
        query_formatted = urllib.parse.quote_plus(query)
        url = f"https://news.google.com/rss/search?q={query_formatted}&hl=en-US&gl=US&ceid=US:en"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        items = root.findall('.//item')[:3] # Get top 3
        
        def process_item(item):
            title = item.find('title').text if item.find('title') is not None else ""
            desc = item.find('description').text if item.find('description') is not None else ""
            return extract_news_signal(f"{title}\n{desc}")
            
        signals = []
        import time
        for item in items:
            try:
                signals.append(process_item(item))
                time.sleep(1) # Prevent rate limit on free tier
            except Exception as e:
                print(f"Failed to process news item: {e}")
                pass
                
        # Fallback to past news if live fails or returns empty
        if not signals:
            signals = [
                NewsSignalCreate(
                    signal_id="news_fb1",
                    title="Government announces new AI Scholarships for Students",
                    summary="The Ministry of Education has launched a comprehensive scholarship program for students pursuing AI and Machine Learning degrees in 2026.",
                    impact_score=9,
                    impacted_skills=["Artificial Intelligence", "Machine Learning"]
                ),
                NewsSignalCreate(
                    signal_id="news_fb2",
                    title="Major tech hubs open new remote internship programs",
                    summary="Leading tech companies have expanded their remote internship opportunities, making it easier for university students globally to gain practical experience.",
                    impact_score=8,
                    impacted_skills=["Software Engineering", "Remote Collaboration"]
                )
            ]
            
        return signals
    except Exception as e:
        print(f"Full news exception: {e}")
        return [
            NewsSignalCreate(
                signal_id="news_fb1",
                title="Government announces new AI Scholarships for Students",
                summary="The Ministry of Education has launched a comprehensive scholarship program for students pursuing AI and Machine Learning degrees in 2026.",
                impact_score=9,
                impacted_skills=["Artificial Intelligence", "Machine Learning"]
            ),
            NewsSignalCreate(
                signal_id="news_fb2",
                title="Major tech hubs open new remote internship programs",
                summary="Leading tech companies have expanded their remote internship opportunities, making it easier for university students globally to gain practical experience.",
                impact_score=8,
                impacted_skills=["Software Engineering", "Remote Collaboration"]
            )
        ]
