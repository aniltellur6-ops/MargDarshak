import sys
import os
import asyncio
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from backend.app.orchestrator.workflow import margdarshak_app
from backend.app.ontology.skill_graph import SkillGraphManager

load_dotenv()

# Initialize FastMCP Server
mcp = FastMCP("MargDarshak Career Intelligence Server")

@mcp.tool()
async def analyze_career_gap(profile_text: str, job_text: str) -> str:
    """
    Analyzes a student's resume against a job description using the MargDarshak LangGraph Orchestrator.
    Returns the exact missing skills prioritized by Neo4j graph dependencies.
    """
    initial_state = {
        "raw_profile_text": profile_text,
        "raw_job_text": job_text,
        "profile": None,
        "job": None,
        "gaps": None,
        "priorities": None
    }
    
    # Run the orchestrator graph
    final_state = margdarshak_app.invoke(initial_state)
    priorities = final_state.get("priorities", [])
    
    if not priorities:
        return "No skill gaps found. The candidate perfectly matches the job!"
        
    result_lines = ["PRIORITIZED SKILL GAPS:"]
    for idx, p in enumerate(priorities):
        result_lines.append(f"{idx+1}. {p.skill_id} (Score: {p.priority_score:.2f}) - {p.reason}")
        
    return "\n".join(result_lines)

@mcp.tool()
async def get_canonical_skills() -> str:
    """
    Queries the Neo4j Skill Graph to return all canonical skills currently tracked by the system.
    """
    manager = SkillGraphManager()
    query = "MATCH (s:Skill) RETURN s.skill_id as skill, s.name as name, s.category as category"
    
    try:
        with manager.driver.session() as session:
            result = session.run(query)
            skills = [f"- {record['skill']}: {record['name']} ({record['category']})" for record in result]
            return "Canonical Skills in Graph:\n" + "\n".join(skills)
    except Exception as e:
        return f"Failed to query graph: {e}"
    finally:
        manager.close()

if __name__ == "__main__":
    # Run the MCP server over standard I/O (this is how Claude Desktop connects)
    print("Starting MargDarshak MCP Server on stdio...")
    mcp.run()
