import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Optional

class JobExtractionResult(BaseModel):
    title: str = Field(description="The job title")
    company: str = Field(description="The name of the company hiring")
    location: Optional[str] = Field(description="Job location if mentioned")
    description: str = Field(description="A brief summary of the role")
    must_have_skills: List[str] = Field(description="List of skills explicitly stated as required or mandatory")
    nice_to_have_skills: List[str] = Field(description="List of skills stated as preferred, a plus, or nice to have")

def extract_job(raw_text: str) -> JobExtractionResult:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert HR and Career Agent. Your goal is to extract a structured Job Description from raw text.\n"
                   "Categorize the skills strictly into 'must_have_skills' and 'nice_to_have_skills'.\n"
                   "Return raw string names for the skills (e.g., 'React.js', 'Spring Boot'). We will normalize them later."),
        ("human", "Extract the job details from the following text:\n\n{text}")
    ])
    
    chain = prompt | llm.with_structured_output(JobExtractionResult)
    result = chain.invoke({"text": raw_text})
    
    return result
