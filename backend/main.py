from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from routers.job_skills import router as job_skills_router
from database import engine, SessionLocal
from models.skill import Skill
from models.education import Education
from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.skills import router as skills_router
from models.user_skill import UserSkill
from routers.jobs import router as jobs_router
from routers import recommendations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(recommendations.router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(skills_router)
app.include_router(jobs_router) 
app.include_router(job_skills_router)

@app.get("/")
def root():
    return {
        "message": "Intelligent Job Recommendation System API is running"
    }


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/api/database-test")
def database_test():
    connection = engine.connect()
    connection.close()

    return {
        "message": "Database connection successful"
    }


