import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from backend.app.services.job_service import parse_and_normalize_job

load_dotenv()

dummy_jd = \"\"\"
We are looking for a Backend Engineer to join our team at TechCorp.
Location: Remote

Responsibilities:
- Build scalable APIs
- Manage database architecture

Required Skills:
- 3+ years of experience in Java
- Strong knowledge of Springboot and REST APIs
- SQL database management

Nice to have:
- Experience with docker and containerization
- React.js frontend knowledge
\"\"\"

def run_test():
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. Cannot run LLM extraction test.")
        return

    print("Running Job Extraction and Normalization...")
    job = parse_and_normalize_job(dummy_jd)
    print("\nNormalized Job Result:")
    print(job.model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
