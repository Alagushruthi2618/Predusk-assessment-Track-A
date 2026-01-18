from fastapi import FastAPI, HTTPException, Depends, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv

from database import get_db, engine
from models import Base, Profile, Skill, Project
from schemas import ProfileCreate, ProfileResponse, SkillResponse, ProjectResponse, SearchResponse
from seed import seed_database

load_dotenv()

API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

app = FastAPI(
    title="Me-API Playground",
    description="A simple API to showcase personal profile, projects, and skills",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    seed_database()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/profile", response_model=ProfileResponse)
async def get_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.put("/profile", response_model=ProfileResponse)
async def update_profile(profile_data: ProfileCreate, db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    profile = db.query(Profile).first()
    if not profile:
        profile = Profile(**profile_data.dict())
        db.add(profile)
    else:
        for field, value in profile_data.dict().items():
            setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@app.get("/skills", response_model=List[SkillResponse])
async def get_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    return skills

@app.get("/skills/top", response_model=List[SkillResponse])
async def get_top_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).order_by(Skill.level.desc()).limit(5).all()
    return skills

@app.get("/projects", response_model=List[ProjectResponse])
async def get_projects(skill: Optional[str] = Query(None), limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    query = db.query(Project)
    
    if skill:
        query = query.join(Project.skills).filter(Skill.name.ilike(f"%{skill}%"))
    
    projects = query.offset(offset).limit(limit).all()
    return projects

@app.get("/search", response_model=List[SearchResponse])
async def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    
    search_term = f"%{q}%"
    
    projects = db.query(Project).filter(
        (Project.title.ilike(search_term)) |
        (Project.description.ilike(search_term))
    ).all()
    
    skills = db.query(Skill).filter(Skill.name.ilike(search_term)).all()
    
    results = []
    
    for project in projects:
        results.append(SearchResponse(
            type="project",
            id=project.id,
            title=project.title,
            description=project.description
        ))
    
    for skill in skills:
        results.append(SearchResponse(
            type="skill",
            id=skill.id,
            title=skill.name,
            description=f"Skill level: {skill.level}"
        ))
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
