# 🧭 MargDarshak Intelligence Backend

MargDarshak is an agentic career platform that converts a student's current profile and career goal into an evidence-based, continuously updated path toward relevant employment opportunities.

It uses an advanced **LangGraph-driven Orchestrator**, powered by OpenAI structured extraction and a persistent **Neo4j Canonical Skill Graph**, to identify precisely what skills a student possesses, what a job requires, and how to bridge the gap with prioritized courses and projects.

## 🏗️ Architecture

The backend consists of 14+ highly intelligent micro-agents, orchestrated into a unified LangGraph state machine:

1. **Profile Intelligence**: Extracts structured skills and evidence from messy resumes.
2. **Skill Ontology (Neo4j)**: Canonicalizes raw skill names into a strict Neo4j Graph hierarchy.
3. **Job Intelligence**: Analyzes job descriptions for required skills.
4. **Matching Engine**: Computes exact overlap between a Profile and a Job.
5. **Gap Analysis**: Determines exactly which skills the student is missing.
6. **Gap Prioritization**: Ranks missing skills based on Neo4j dependencies (e.g., learn Python before K8s).
7. **Opportunity Engine**: Matches student to new jobs automatically.
8. **Course & Project Intelligence**: Recommends ways to fill the gaps.
9. **Assessment & Progress Engines**: Generates quizzes and updates skill proficiencies dynamically.
10. **News Intelligence**: Analyzes market trends and updates the Neo4j Skill Graph dynamically!
11. **Agent Orchestrator (LangGraph)**: Strings all the above together automatically.
12. **Graph Memory**: Persists Students and Jobs into Neo4j.
13. **System Orchestrator**: Hardened REST API serving all intelligence layer endpoints.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- Neo4j Desktop or Neo4j Aura DB

### 2. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/aniltellur6-ops/MargDarshak.git
cd MargDarshak
pip install -r requirements.txt
```

### 3. Environment Setup

Copy the example environment file and insert your keys:

```bash
cp .env.example .env
```

Ensure `.env` contains valid keys for OpenAI and Neo4j.

### 4. Running the Server

Start the unified FastAPI system orchestrator:

```bash
cd backend
uvicorn app.main:app --reload
```

The Swagger UI documentation will be available at: `http://127.0.0.1:8000/docs`
