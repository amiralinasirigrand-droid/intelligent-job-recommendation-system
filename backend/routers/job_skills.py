from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.job import Job
from models.job_skill import JobSkill
from schemas.job_skill import JobSkillCreate, JobSkillResponse
from schemas.job_skill import (
    JobSkillCreate,
    JobSkillResponse,
    JobSkillDetailResponse,
    JobSkillUpdate
)
from models.skill import Skill


router = APIRouter(
    prefix="/api/jobs",
    tags=["Job Skills"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{job_id}/skills", response_model=JobSkillResponse)
def add_job_skill(
    job_id: int,
    skill: JobSkillCreate,
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

    existing_skill = db.query(JobSkill).filter(
        JobSkill.job_id == job_id,
        JobSkill.skill_id == skill.skill_id
    ).first()

    if existing_skill:
        raise HTTPException(
            status_code=400,
            detail="Skill already added to this job"
        )

    new_job_skill = JobSkill(
        job_id=job_id,
        skill_id=skill.skill_id,
        required_level=skill.required_level,
        is_required=skill.is_required
    )

    db.add(new_job_skill)
    db.commit()
    db.refresh(new_job_skill)

    return new_job_skill

@router.get(
    "/{job_id}/skills",
    response_model=list[JobSkillDetailResponse]
)
def get_job_skills(
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

    return [
        {
            "job_id": job_skill.job_id,
            "skill_id": job_skill.skill_id,
            "skill_name": skill_name,
            "required_level": job_skill.required_level,
            "is_required": job_skill.is_required
        }
        for job_skill, skill_name in job_skills
    ]

@router.delete("/{job_id}/skills/{skill_id}")
def delete_job_skill(
    job_id: int,
    skill_id: int,
    db: Session = Depends(get_db)
):
    job_skill = db.query(JobSkill).filter(
        JobSkill.job_id == job_id,
        JobSkill.skill_id == skill_id
    ).first()

    if not job_skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found for this job"
        )

    db.delete(job_skill)
    db.commit()

    return {
        "message": "Skill removed from job successfully"
    }

@router.put(
    "/{job_id}/skills/{skill_id}",
    response_model=JobSkillResponse
)
def update_job_skill(
    job_id: int,
    skill_id: int,
    skill: JobSkillUpdate,
    db: Session = Depends(get_db)
):
    job_skill = db.query(JobSkill).filter(
        JobSkill.job_id == job_id,
        JobSkill.skill_id == skill_id
    ).first()

    if not job_skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found for this job"
        )

    job_skill.required_level = skill.required_level
    job_skill.is_required = skill.is_required

    db.commit()
    db.refresh(job_skill)

    return job_skill