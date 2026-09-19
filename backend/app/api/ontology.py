from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.ontology.skill_graph import SkillGraphManager

router = APIRouter()
manager = SkillGraphManager()

class NormalizeRequest(BaseModel):
    raw_skills: List[str]

class NormalizeResponse(BaseModel):
    normalized: dict[str, Optional[str]]

@router.post("/normalize", response_model=NormalizeResponse)
async def normalize_skills(req: NormalizeRequest):
    result = {}
    for skill in req.raw_skills:
        canonical_id = manager.normalize_skill(skill)
        result[skill] = canonical_id
    return NormalizeResponse(normalized=result)
