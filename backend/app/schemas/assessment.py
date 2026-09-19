from pydantic import BaseModel, Field
from typing import List

class QuizQuestion(BaseModel):
    question_text: str
    options: List[str] = Field(description="Exactly 4 multiple choice options", min_length=4, max_length=4)
    correct_option_index: int = Field(description="Index of the correct option (0-3)", ge=0, le=3)
    explanation: str = Field(description="Brief explanation of why this is the correct answer")

class AssessmentQuiz(BaseModel):
    skill_id: str
    difficulty: str
    questions: List[QuizQuestion]
