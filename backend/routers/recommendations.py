
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.job import Job
from models.job_skill import JobSkill
from models.skill import Skill
from models.user_skill import UserSkill
from routers.users import get_current_user
from services.recommendation import calculate_skill_match


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/me")
def get_my_recommendations(
    location: str | None = None,
    employment_type: str | None = None,
    title: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # 1. Get the current user's skills and proficiency levels
    user_skills = db.query(
        UserSkill.skill_id,
        UserSkill.skill_level
    ).filter(
        UserSkill.user_id == current_user.id
    ).all()

    user_skill_levels = {
        row.skill_id: row.skill_level
        for row in user_skills
    }

    user_skill_ids = set(user_skill_levels.keys())

    # 2. Build the job query and apply optional filters
    jobs_query = db.query(Job)

    if location:
        jobs_query = jobs_query.filter(
            Job.location.ilike(f"%{location}%")
        )

    if employment_type:
        jobs_query = jobs_query.filter(
            Job.employment_type.ilike(employment_type)
        )

    if title:
        jobs_query = jobs_query.filter(
            Job.title.ilike(f"%{title}%")
        )

    jobs = jobs_query.all()
    recommendations = []

    # 3. Calculate the match score for each filtered job
    for job in jobs:
        job_skill_rows = db.query(
            JobSkill.skill_id,
            JobSkill.is_required,
            JobSkill.required_level,
            Skill.name
        ).join(
            Skill,
            Skill.id == JobSkill.skill_id
        ).filter(
            JobSkill.job_id == job.id
        ).all()

        job_skills = [
            {
                "skill_id": row.skill_id,
                "is_required": row.is_required,
                "required_level": row.required_level,
                "user_level": user_skill_levels.get(row.skill_id),
                "name": row.name,
            }
            for row in job_skill_rows
        ]

        match_result = calculate_skill_match(
            user_skill_ids,
            job_skills
        )

        skill_names = {
            row.skill_id: row.name
            for row in job_skill_rows
        }

        recommendations.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "employment_type": job.employment_type,
            "match_score": match_result["match_score"],
            "explanations": match_result["explanations"],
            "matched_skills": [
                skill_names[skill_id]
                for skill_id in match_result["matched_skills"]
            ],
            "missing_skills": [
                skill_names[skill_id]
                for skill_id in match_result["missing_skills"]
            ],
            "matched_required_skills": [
                skill_names[skill_id]
                for skill_id in match_result["matched_required_skills"]
            ],
            "missing_required_skills": [
                skill_names[skill_id]
                for skill_id in match_result["missing_required_skills"]
            ],
            "matched_optional_skills": [
                skill_names[skill_id]
                for skill_id in match_result["matched_optional_skills"]
            ],
            "missing_optional_skills": [
                skill_names[skill_id]
                for skill_id in match_result["missing_optional_skills"]
            ],
        })

    # 4. Show the best-matching jobs first
    recommendations.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return recommendations

@router.get("/jobs/{job_id}")
def get_job_match_details(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # 1. Find the requested job
    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # 2. Get the user's skills and their levels
    user_skills = db.query(
        UserSkill.skill_id,
        UserSkill.skill_level
    ).filter(
        UserSkill.user_id == current_user.id
    ).all()

    user_skill_levels = {
        row.skill_id: row.skill_level
        for row in user_skills
    }

    user_skill_ids = set(user_skill_levels.keys())

    # 3. Get the skills required by this job
    job_skill_rows = db.query(
        JobSkill.skill_id,
        JobSkill.is_required,
        JobSkill.required_level,
        Skill.name,
        Skill.description
    ).join(
        Skill,
        Skill.id == JobSkill.skill_id
    ).filter(
        JobSkill.job_id == job_id
    ).all()

    job_skills = [
        {
            "skill_id": row.skill_id,
            "is_required": row.is_required,
            "required_level": row.required_level,
            "user_level": user_skill_levels.get(row.skill_id),
            "name": row.name,
        }
        for row in job_skill_rows
    ]

    # 4. Calculate the match using the existing algorithm
    match_result = calculate_skill_match(
        user_skill_ids,
        job_skills
    )

    # 5. Build detailed information for each skill
    skill_details = []

    for row in job_skill_rows:
        skill_details.append({
            "skill_id": row.skill_id,
            "skill_name": row.name,
            "description": row.description,
            "user_level": user_skill_levels.get(row.skill_id),
            "required_level": row.required_level,
            "is_required": row.is_required,
            "is_present": row.skill_id in user_skill_ids,
        })
    
    # 6. Generate learning recommendations
    level_scores = {
        "beginner": 25,
        "intermediate": 50,
        "advanced": 100,
    }

    learning_recommendations = []

    for row in job_skill_rows:
        user_level = user_skill_levels.get(row.skill_id)
        required_level = row.required_level

        # No recommendation is needed if no level was specified
        if not required_level:
            continue

        required_score = level_scores.get(
            required_level.lower(), 0
        )

        user_score = level_scores.get(
            user_level.lower() if user_level else "", 0
        )

        # Skip skills for which the user already meets the requirement
        if user_score >= required_score and required_score > 0:
            continue

        if not user_level:
            recommendation_type = "learn"
            message = (
                f"Learn {row.name} to reach the "
                f"{required_level} level."
            )
        else:
            recommendation_type = "improve"
            message = (
                f"Improve your {row.name} skills from "
                f"{user_level} to {required_level}."
            )

        learning_recommendations.append({
            "skill_id": row.skill_id,
            "skill_name": row.name,
            "current_level": user_level,
            "required_level": required_level,
            "is_required": row.is_required,
            "priority": "high" if row.is_required else "medium",
            "recommendation_type": recommendation_type,
            "message": message,
        })

    # Required skills should appear before optional skills
    learning_recommendations.sort(
        key=lambda item: (
            item["priority"] != "high",
            item["skill_name"].lower()
        )
    )


    # 6. Return job information and match results
    return {
        "job_id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "employment_type": job.employment_type,
        "description": job.description,
        "match_score": match_result["match_score"],
        "matched_skills": [
            row.name
            for row in job_skill_rows
            if row.skill_id in match_result["matched_skills"]
        ],
        "missing_required_skills": [
            row.name
            for row in job_skill_rows
            if row.skill_id in match_result["missing_required_skills"]
        ],
        "missing_optional_skills": [
            row.name
            for row in job_skill_rows
            if row.skill_id in match_result["missing_optional_skills"]
        ],
        "explanations": match_result["explanations"],
        "skill_details": skill_details,
        "learning_recommendations": learning_recommendations,
    }
