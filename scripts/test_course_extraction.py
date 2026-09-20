import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from agents.course.extractor import extract_course

load_dotenv()

def run_test():
    raw_course_text = """
    Welcome to the 2024 Ultimate Backend Bootcamp on Udemy!
    In this course, you will learn everything you need to become a backend engineer.
    We will cover programming in Python, building APIs, and storing data in Postgres.
    Finally, you will learn how to deploy your applications using K8s and containerization!
    """
    
    print("Running Course Intelligence Extraction...")
    course = extract_course(raw_course_text)
    
    print("\nExtracted Canonical Course:")
    print(course.model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
