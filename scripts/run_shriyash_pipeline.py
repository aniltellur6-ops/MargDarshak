import os
import sys
import json
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from backend.app.orchestrator.workflow import margdarshak_app

load_dotenv()

def run_test():
    raw_profile = """
    SHRIYASH ANIL TELLUR
    Third-year B.Tech (IT) student with hands-on experience building two end-to-end RAG-based AI systems.
    EDUCATION: B.Tech, Information Technology — Walchand Institute of Technology, Solapur 2024 – Present (3rd Year)
    KEY SKILLS:
    Critical Thinking & Analysis, Leadership & Management, Communication, Team Dynamics
    Technical: RAG/LLM App Development (LangChain, ChromaDB, Gemini/OpenAI) · Python & Streamlit · SQLite
    PROJECTS:
    RecycleAI – Smart Recycling Assistant — RAG + Computer Vision + ChromaDB. AI platform that identifies waste materials from photos and generates safe, structured recycling instructions via a full RAG pipeline (ingestion, MiniLM embeddings, multi-query retrieval, optional Cohere reranking, hazard/safety guardrails).
    Healthcare Monitoring AI Agent — Python, Streamlit, LangChain, RAG. Health assistant for medication tracking, smart reminders, and an AI chatbot delivering safe, non-diagnostic guidance; SQLite-backed data model for medications, logs, and reminders.
    VacSort — Smart AI Bin — Civic-Tech Innovation Project (Hardware + Software). Developing a solution for a major societal problem.
    EXPERIENCE: Assistant Leader (Marketing & Sales) — Zoopy India Pvt. Ltd.
    """
    
    raw_job = """
    Role: AI/ML Engineer (FAANG)
    Responsibilities:
    Design, train, and deploy large-scale machine learning models and LLMs.
    Requirements:
    - Strong proficiency in Python, C++, or Java.
    - Experience with Deep Learning frameworks like PyTorch or TensorFlow.
    - Knowledge of cloud infrastructure (AWS/GCP), Docker, and Kubernetes (K8s).
    - Solid understanding of algorithms, data structures, and system design.
    - Experience in deploying ML models into production (MLOps, CI/CD).
    - Familiarity with Vector Databases and LLM orchestration frameworks (LangChain, LlamaIndex).
    """
    
    print("Running MargDarshak Orchestrator End-to-End for Shriyash...")
    
    initial_state = {
        "raw_profile_text": raw_profile,
        "raw_job_text": raw_job,
        "profile": None,
        "job": None,
        "gaps": None,
        "priorities": None
    }
    
    final_state = margdarshak_app.invoke(initial_state)
    
    print("\n================== PROFILE EXTRACTED ==================")
    if final_state.get("profile"):
        print(final_state["profile"].model_dump_json(indent=2))
        
    print("\n================== JOB EXTRACTED ==================")
    if final_state.get("job"):
        print(final_state["job"].model_dump_json(indent=2))
        
    print("\n================== IDENTIFIED GAPS ==================")
    if final_state.get("gaps"):
        print(final_state["gaps"].model_dump_json(indent=2))
            
    print("\n================== PRIORITIZED GAPS ==================")
    if final_state.get("priorities"):
        print(final_state["priorities"].model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
