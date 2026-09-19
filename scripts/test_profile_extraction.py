import os
import sys
from dotenv import load_dotenv
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from agents.profile.extractor import extract_profile

load_dotenv()

dummy_resume = \"\"\"
John Doe
Location: Pune, India
Education: B.Tech in Information Technology, XYZ College (2020-2024)
Target Role: Backend Developer

Skills:
- Java
- Spring Boot
- SQL
- React

Experience / Projects:
1. Hospital Management System
Built a full-stack web application using Java, Spring Boot, and SQL. Deployed on AWS.
2. Academic Portal
Created a student portal frontend using React.
\"\"\"

def run_test():
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. Cannot run LLM extraction test.")
        return

    print("Running Profile Extraction...")
    result = extract_profile(dummy_resume)
    print("\nExtraction Result:")
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
