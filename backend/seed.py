from sqlalchemy.orm import Session
from models import Profile, Skill, Project
from database import SessionLocal


def seed_database():
    db: Session = SessionLocal()

    try:
        # Prevent reseeding
        if db.query(Profile).first():
            print("Database already seeded. Skipping.")
            return

        # ---------------- PROFILE ----------------
        profile = Profile(
            name="Alagu Shruthi",
            email="kralagushruthi@gmail.com",
            education="B.Tech in Computer Science and Engineering, NIT Delhi",
            bio=(
                "Final-year Computer Science student at NIT Delhi with hands-on experience building "
                "production-grade backend APIs and AI-assisted systems. Interned at Plooran, where I "
                "shipped modular frontend features, integrated authentication flows, and worked in a "
                "fast-paced startup environment. Built projects spanning cybersecurity (IDS), "
                "data-driven applications (Expense Tracker), and AI-powered intent classification. "
                "Actively interested in backend engineering, retrieval-based AI systems, and reliable "
                "software design."
            ),
            github="https://github.com/Alagushruthi2618",
            linkedin="https://www.linkedin.com/in/alagu-shruthi-karuppan-chetty-30b047299/",
        )

        # ---------------- SKILLS ----------------
        skills_data = [
            ("Python", "Advanced"),
            ("FastAPI", "Advanced"),
            ("Flask", "Advanced"),
            ("REST APIs", "Advanced"),
            ("JavaScript", "Advanced"),
            ("HTML/CSS", "Advanced"),
            ("SQL", "Intermediate"),
            ("Git", "Advanced"),
            ("Docker", "Beginner"),
            ("AI / LLM Integration", "Beginner"),
            ("Cybersecurity", "Intermediate"),
        ]

        skills = []
        for name, level in skills_data:
            skill = Skill(name=name, level=level)
            db.add(skill)
            skills.append(skill)

        # Flush to generate IDs before relationships
        db.flush()

        skill_map = {skill.name: skill for skill in skills}

        # ---------------- PROJECTS ----------------
        projects_data = [
            {
                "title": "Intrusion Detection System (IDS)",
                "description": (
                    "Network-based Intrusion Detection System developed as a cybersecurity project. "
                    "Implemented packet inspection and rule-based anomaly detection to identify "
                    "suspicious network behavior. Focused on understanding traffic patterns, "
                    "false positives, and detection accuracy."
                ),
                "github_url": "https://github.com/Alagushruthi2618/ML_project",
                "live_url": None,
                "skill_names": ["Python", "Cybersecurity"],
            },
            {
                "title": "Expense Tracker Application",
                "description": (
                    "Backend-driven expense tracking application that supports recording, "
                    "categorizing, and querying user expenses. Designed REST APIs for CRUD "
                    "operations, handled data persistence with SQL, and implemented basic "
                    "aggregation queries for expense summaries."
                ),
                "github_url": "https://github.com/Alagushruthi2618/Expense-Tracker",
                "live_url": None,
                "skill_names": ["Python", "SQL", "REST APIs"],
            },
            {
                "title": "Wedding Album Web Platform (Plooran)",
                "description": (
                    "Frontend-focused web platform for managing and showcasing wedding albums. "
                    "Implemented modular UI components, authentication flows, SEO improvements, "
                    "and responsive design using JavaScript and Flask-based backend integration."
                ),
                "github_url": None,
                "live_url": None,
                "skill_names": ["JavaScript", "Flask", "HTML/CSS", "REST APIs"],
            },
            {
                "title": "Debt Collection Web Agent",
                "description": (
                    "Chat-based web application for automated debt collection workflows. "
                    "Worked on frontend-backend integration, UI improvements, chat flow handling, "
                    "and user interaction logic in a startup environment."
                ),
                "github_url": "https://github.com/Alagushruthi2618/Debt-Collection-web-Agent",
                "live_url": None,
                "skill_names": ["JavaScript", "FastAPI", "REST APIs"],
            },
            {
                "title": "AI-Powered Chat & Intent Classification System",
                "description": (
                    "AI-driven intent classification system built using LLM APIs. Implemented "
                    "structured prompts, fallback strategies, and backend integration to route "
                    "user queries and generate contextual responses."
                ),
                "github_url": None,
                "live_url": None,
                "skill_names": ["Python", "AI / LLM Integration", "FastAPI"],
            },
            {
                "title": "Personal Portfolio & API Playground",
                "description": (
                    "Backend REST API exposing personal profile, skills, and projects. "
                    "Includes database schema design, filtering and search endpoints, "
                    "health checks, and a minimal frontend client."
                ),
                "github_url": None,
                "live_url": None,
                "skill_names": ["Python", "FastAPI", "SQL", "Git"],
            },
        ]

        for data in projects_data:
            project = Project(
                title=data["title"],
                description=data["description"],
                github_url=data["github_url"],
                live_url=data["live_url"],
            )

            for skill_name in data["skill_names"]:
                project.skills.append(skill_map[skill_name])

            db.add(project)

        db.add(profile)
        db.commit()

        print("Database seeded successfully with enhanced portfolio data.")

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
