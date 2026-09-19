import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from agents.assessment.generator import generate_assessment

load_dotenv()

def run_test():
    skill_to_test = "KUBERNETES"
    difficulty = "Intermediate"
    
    print(f"Generating dynamic Assessment for {skill_to_test} at {difficulty} level...")
    quiz = generate_assessment(skill_to_test, difficulty)
    
    print("\nGenerated Quiz:")
    print(f"Skill: {quiz.skill_id}")
    for i, q in enumerate(quiz.questions):
        print(f"\nQ{i+1}: {q.question_text}")
        for j, opt in enumerate(q.options):
            print(f"  [{j}] {opt}")
        print(f"Answer: [{q.correct_option_index}] -> {q.options[q.correct_option_index]}")
        print(f"Explanation: {q.explanation}")

if __name__ == "__main__":
    run_test()
