from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User
from models.job import Job
from schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobDetailResponse
)
from models.job_skill import JobSkill
from models.skill import Skill
from routers.users import get_current_user


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=JobResponse)
def create_job(
    job: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_job = Job(
        title=job.title,
        company=job.company,
        description=job.description,
        location=job.location,
        employment_type=job.employment_type
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@router.get("/", response_model=list[JobResponse])
def get_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).all()

    return jobs

@router.get("/{job_id}", response_model=JobDetailResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job_skills = db.query(
        JobSkill,
        Skill.name
    ).join(
        Skill,
        JobSkill.skill_id == Skill.id
    ).filter(
        JobSkill.job_id == job_id
    ).all()

    skills = [
        {
            "job_id": job_skill.job_id,
            "skill_id": job_skill.skill_id,
            "skill_name": skill_name,
            "required_level": job_skill.required_level,
            "is_required": job_skill.is_required
        }
        for job_skill, skill_name in job_skills
    ]

    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "location": job.location,
        "employment_type": job.employment_type,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
        "skills": skills
    }

@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db)
):
    existing_job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not existing_job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    existing_job.title = job.title
    existing_job.company = job.company
    existing_job.description = job.description
    existing_job.location = job.location
    existing_job.employment_type = job.employment_type

    db.commit()
    db.refresh(existing_job)

    return existing_job

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    existing_job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not existing_job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(existing_job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }