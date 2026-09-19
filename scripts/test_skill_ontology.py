import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from app.ontology.skill_graph import SkillGraphManager

def run_test():
    manager = SkillGraphManager()
    
    test_cases = ["ReactJS", "java", "Spring-boot", "Unknown Skill"]
    
    print("Normalizing Skills:")
    for skill in test_cases:
        norm = manager.normalize_skill(skill)
        print(f"'{skill}' -> {norm}")

if __name__ == "__main__":
    run_test()
