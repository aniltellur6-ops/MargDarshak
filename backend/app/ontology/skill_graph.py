from neo4j import GraphDatabase
from typing import List, Dict, Optional
import os

class SkillGraphManager:
    def __init__(self, uri=None, user=None, password=None):
        uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = user or os.getenv("NEO4J_USER", "neo4j")
        password = password or os.getenv("NEO4J_PASSWORD", "margdarshak_secret")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_skill(self, skill_id: str, name: str, category: str):
        query = (
            "MERGE (s:Skill {skill_id: }) "
            "SET s.name = , s.category =  "
            "RETURN s"
        )
        with self.driver.session() as session:
            session.run(query, skill_id=skill_id, name=name, category=category)

    def add_alias(self, alias_name: str, skill_id: str):
        query = (
            "MERGE (a:Alias {name: }) "
            "WITH a "
            "MATCH (s:Skill {skill_id: }) "
            "MERGE (a)-[:MAPS_TO]->(s)"
        )
        with self.driver.session() as session:
            session.run(query, alias_name=alias_name.lower(), skill_id=skill_id)

    def add_parent(self, child_id: str, parent_id: str):
        query = (
            "MATCH (c:Skill {skill_id: }) "
            "MATCH (p:Skill {skill_id: }) "
            "MERGE (p)-[:PARENT_OF]->(c)"
        )
        with self.driver.session() as session:
            session.run(query, child_id=child_id, parent_id=parent_id)

    def add_relationship(self, source_id: str, target_id: str, rel_type: str):
        # We need to construct the query string to inject the relationship type securely
        # but safely as neo4j doesn't parameterize relationship types
        valid_rels = ["REQUIRES", "RELATED_TO"]
        if rel_type not in valid_rels:
            raise ValueError(f"Invalid relationship type: {rel_type}")
            
        query = (
            f"MATCH (s:Skill {{skill_id: }}) "
            f"MATCH (t:Skill {{skill_id: }}) "
            f"MERGE (s)-[:{rel_type}]->(t)"
        )
        with self.driver.session() as session:
            session.run(query, source_id=source_id, target_id=target_id)

    def normalize_skill(self, raw_skill_name: str) -> Optional[str]:
        query = (
            "MATCH (a:Alias {name: })-[:MAPS_TO]->(s:Skill) "
            "RETURN s.skill_id AS skill_id LIMIT 1"
        )
        with self.driver.session() as session:
            result = session.run(query, alias_name=raw_skill_name.lower())
            record = result.single()
            if record:
                return record["skill_id"]
        return None


    def calculate_similarity(self, skill_a_id: str, skill_b_id: str) -> float:
        if not skill_a_id or not skill_b_id:
            return 0.0
            
        skill_a = skill_a_id.upper()
        skill_b = skill_b_id.upper()
        
        if skill_a == skill_b:
            return 1.0
            
        query = (
            "MATCH (a:Skill {skill_id: }), (b:Skill {skill_id: }) "
            "OPTIONAL MATCH (a)-[p:PARENT_OF]-(b) "
            "OPTIONAL MATCH (a)-[r:RELATED_TO|REQUIRES]-(b) "
            "RETURN p, r"
        )
        with self.driver.session() as session:
            result = session.run(query, skill_a=skill_a, skill_b=skill_b)
            record = result.single()
            if record:
                if record["p"] is not None:
                    return 0.8
                if record["r"] is not None:
                    return 0.5
        return 0.0


    def get_skill_dependency_weight(self, skill_id: str) -> int:
        if not skill_id:
            return 0
            
        # Count how many other skills have a REQUIRES or PARENT_OF pointing to this skill
        query = (
            "MATCH (other:Skill)-[:REQUIRES|PARENT_OF]->(target:Skill {skill_id: }) "
            "RETURN count(other) AS dep_count"
        )
        with self.driver.session() as session:
            result = session.run(query, skill_id=skill_id.upper())
            record = result.single()
            if record:
                return record["dep_count"]
        return 0

    def clear_database(self):
        query = "MATCH (n) DETACH DELETE n"
        with self.driver.session() as session:
            session.run(query)


