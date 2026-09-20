import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from agents.project.extractor import extract_project

load_dotenv()

def run_test():
    raw_project_text = """
    I built a highly scalable microservices architecture for an e-commerce platform.
    The main backend is written in Python using FastAPI. For the database, I used Postgres.
    Everything is containerized and deployed using K8s on AWS.
    """
    
    print("Running Project Intelligence Extraction...")
    project = extract_project(raw_project_text)
    
    print("\nExtracted Canonical Project:")
    print(project.model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
