import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.schemas.assessment import AssessmentQuiz, QuizQuestion

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_assessment(skill_id: str, difficulty: str = "Intermediate") -> AssessmentQuiz:
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.2)
    structured_llm = llm.with_structured_output(AssessmentQuiz)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert technical examiner. The user needs to prove they know the technical skill '{skill_id}' at a '{difficulty}' level. Generate exactly 3 highly technical, unambiguous multiple-choice questions to test their knowledge. Provide exactly 4 options per question, the index of the correct option, and a brief educational explanation."),
    ])
    
    chain = prompt | structured_llm
    
    # Generate the quiz
    quiz = chain.invoke({
        "skill_id": skill_id,
        "difficulty": difficulty
    })
    
    # Ensure metadata is correct
    quiz.skill_id = skill_id.upper()
    quiz.difficulty = difficulty
    
    return quiz
