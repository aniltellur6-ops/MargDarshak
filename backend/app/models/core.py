from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    education_degree = Column(String)
    education_branch = Column(String)
    target_role = Column(String)
    target_company = Column(String)
    location = Column(String)
    
    evidences = relationship("SkillEvidence", back_populates="profile")
    progress = relationship("Progress", back_populates="profile", uselist=False)

class SkillEvidence(Base):
    __tablename__ = "skill_evidences"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id"))
    skill_name = Column(String, index=True)
    evidence = Column(String)
    evidence_type = Column(String)
    
    profile = relationship("StudentProfile", back_populates="evidences")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(String, unique=True, index=True)
    name = Column(String)
    category = Column(String)
    parent_id = Column(Integer, ForeignKey("skills.id"), nullable=True)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    role = Column(String)
    company = Column(String)
    location = Column(String)
    
    requirements = relationship("JobRequirement", back_populates="job")

class JobRequirement(Base):
    __tablename__ = "job_requirements"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    skill_name = Column(String)
    is_required = Column(Boolean, default=True)
    
    job = relationship("Job", back_populates="requirements")

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id"))
    backend_readiness = Column(Float, default=0.0)
    matching_jobs_count = Column(Integer, default=0)
    
    profile = relationship("StudentProfile", back_populates="progress")
