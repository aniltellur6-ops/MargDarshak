import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from agents.news.extractor import extract_news_signal

load_dotenv()

def run_test():
    raw_news_text = \"\"\"
    Major enterprise AcmeCorp announced today that they are abandoning their legacy PHP monolith 
    and rewriting their entire backend using Go (Golang) for better concurrency and performance.
    They also plan to migrate their databases to Postgres.
    \"\"\"
    
    print("Running News Intelligence Extraction...")
    signal = extract_news_signal(raw_news_text)
    
    print("\nExtracted Canonical News Signal:")
    print(signal.model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
