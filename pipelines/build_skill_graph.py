import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from app.ontology.skill_graph import SkillGraphManager

def build_graph():
    manager = SkillGraphManager()
    
    print("Clearing existing graph...")
    manager.clear_database()
    
    print("Loading skills...")
    with open("data/skills/skill_taxonomy.json", "r") as f:
        skills = json.load(f)
        for s in skills:
            manager.add_skill(s["skill_id"], s["name"], s.get("category", "General"))
            if "parent" in s:
                manager.add_parent(s["skill_id"], s["parent"])
                
    print("Loading aliases...")
    with open("data/skills/skill_aliases.json", "r") as f:
        aliases = json.load(f)
        for alias, target in aliases.items():
            manager.add_alias(alias, target)
            # Add the target name itself as an alias just in case
            manager.add_alias(target, target)
            
    print("Loading relationships...")
    with open("data/skills/skill_relationships.json", "r") as f:
        rels = json.load(f)
        for r in rels:
            manager.add_relationship(r["source"], r["target"], r["type"])
            
    print("Graph built successfully!")
    manager.close()

if __name__ == "__main__":
    build_graph()
