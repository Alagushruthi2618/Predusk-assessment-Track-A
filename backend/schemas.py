from pydantic import BaseModel
from typing import List, Optional

class ProfileCreate(BaseModel):
    name: str
    email: str
    education: Optional[str] = None
    bio: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    education: Optional[str] = None
    bio: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None
    
    class Config:
        from_attributes = True

class SkillResponse(BaseModel):
    id: int
    name: str
    level: str
    
    class Config:
        from_attributes = True

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    skills: List[SkillResponse] = []
    
    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    type: str  # "project" or "skill"
    id: int
    title: str
    description: str
