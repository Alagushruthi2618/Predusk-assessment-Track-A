from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

project_skills = Table(
    'project_skills',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    education = Column(String(200))
    bio = Column(Text)
    github = Column(String(200))
    linkedin = Column(String(200))
    portfolio = Column(String(200))

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    level = Column(String(20), nullable=False)  # Beginner, Intermediate, Advanced, Expert
    
    projects = relationship("Project", secondary=project_skills, back_populates="skills")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    github_url = Column(String(200))
    live_url = Column(String(200))
    
    skills = relationship("Skill", secondary=project_skills, back_populates="projects")
