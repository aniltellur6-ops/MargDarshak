import os
import sys

# Add backend directory to path so we can import schemas
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.schemas.profile import StudentProfileCreate, SkillEvidence
from pydantic import BaseModel, Field
from typing import List, Optional

# A temporary Pydantic model for Langchain structured output
class ProfileExtractionResult(BaseModel):
    user_id: str = Field(description="A unique placeholder user ID, just use 'generated_user' if unknown.")
    education_degree: Optional[str] = Field(description="The highest education degree (e.g., B.Tech, BSc)")
    education_branch: Optional[str] = Field(description="The education branch or major")
    target_role: Optional[str] = Field(description="The desired target role if mentioned")
    target_company: Optional[str] = Field(description="The desired target company if mentioned")
    location: Optional[str] = Field(description="Current or target location")
    evidences: List[SkillEvidence] = Field(description="List of skills along with their concrete evidence.")

def extract_profile(raw_text: str) -> ProfileExtractionResult:
    # We use Gemini by default. Ensure GOOGLE_API_KEY is in environment.
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Career Profile Intelligence Agent. Your goal is to extract a highly structured profile from a student's resume or free-text description.\n"
                   "CRITICAL INSTRUCTION: For every skill you find, you MUST extract the evidence (e.g., the name of the project, the job experience, or the course where the skill was applied/learned).\n"
                   "Evidence type must be one of: 'project', 'course', 'assessment', 'experience', 'certification'.\n"
                   "Do NOT just list skills without evidence. If a skill has no evidence, do not include it or describe the evidence as 'Self-reported'."),
        ("human", "Extract the profile from the following text:\n\n{text}")
    ])
    
    chain = prompt | llm.with_structured_output(ProfileExtractionResult)
    result = chain.invoke({"text": raw_text})
    
    return result
