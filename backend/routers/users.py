from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.user import User
from models.education import Education
from models.user_skill import UserSkill
from models.skill import Skill

from utils.security import oauth2_scheme, decode_access_token
from database import SessionLocal

from schemas.user import UserResponse
from schemas.education import EducationCreate, EducationResponse, EducationUpdate
from schemas.skill import UserSkillCreate
from models.experience import Experience
from schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceResponse

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_access_token(token)

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/me/education")
def get_my_education(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    educations = db.query(Education).filter(
        Education.user_id == current_user.id
    ).all()

    return educations
@router.get("/me/education/{education_id}", response_model=EducationResponse)
def get_education(
    education_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    education = db.query(Education).filter(
        Education.id == education_id,
        Education.user_id == current_user.id
    ).first()

    if not education:
        raise HTTPException(
            status_code=404,
            detail="Education not found"
        )

    return education
@router.put("/me/education/{education_id}", response_model=EducationResponse)
def update_education(
    education_id: int,
    education: EducationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_education = db.query(Education).filter(
        Education.id == education_id,
        Education.user_id == current_user.id
    ).first()

    if not existing_education:
        raise HTTPException(
            status_code=404,
            detail="Education not found"
        )

    existing_education.degree = education.degree
    existing_education.field_of_study = education.field_of_study
    existing_education.institution = education.institution
    existing_education.start_date = education.start_date
    existing_education.end_date = education.end_date

    db.commit()
    db.refresh(existing_education)

    return existing_education

@router.delete("/me/education/{education_id}")
def delete_education(
    education_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    education = db.query(Education).filter(
        Education.id == education_id,
        Education.user_id == current_user.id
    ).first()

    if not education:
        raise HTTPException(
            status_code=404,
            detail="Education not found"
        )

    db.delete(education)
    db.commit()

    return {
        "message": "Education deleted successfully"
    }


@router.post("/me/education", response_model=EducationResponse)
def add_education(
    education: EducationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_education = Education(
        user_id=current_user.id,
        degree=education.degree,
        field_of_study=education.field_of_study,
        institution=education.institution,
        start_date=education.start_date,
        end_date=education.end_date
    )

    db.add(new_education)
    db.commit()
    db.refresh(new_education)

    return new_education



@router.post("/me/skills")
def add_skill(
    skill: UserSkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_skill = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_id == skill.skill_id
    ).first()

    if existing_skill:
        existing_skill.skill_level = skill.skill_level
        db.commit()
        db.refresh(existing_skill)
        return existing_skill

    new_user_skill = UserSkill(
        user_id=current_user.id,
        skill_id=skill.skill_id,
        skill_level=skill.skill_level
    )

    db.add(new_user_skill)
    db.commit()
    db.refresh(new_user_skill)

    return new_user_skill


@router.get("/me/skills")
def get_my_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skills = db.query(
        Skill.id,
        Skill.name,
        Skill.description,
        UserSkill.skill_level
    ).join(
        UserSkill,
        UserSkill.skill_id == Skill.id
    ).filter(
        UserSkill.user_id == current_user.id
    ).all()

    return [
        {
            "id": skill.id,
            "name": skill.name,
            "description": skill.description,
            "skill_level": skill.skill_level
        }
        for skill in skills
    ]


@router.delete("/me/skills/{skill_id}")
def delete_my_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_id == skill_id
    ).first()

    if not user_skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found for this user"
        )

    db.delete(user_skill)
    db.commit()

    return {
        "message": "Skill deleted successfully"
    }

@router.post("/me/experience", response_model=ExperienceResponse)
def add_experience(
    experience: ExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_experience = Experience(
        user_id=current_user.id,
        job_title=experience.job_title,
        company=experience.company,
        description=experience.description,
        start_date=experience.start_date,
        end_date=experience.end_date
    )

    db.add(new_experience)
    db.commit()
    db.refresh(new_experience)

    return new_experience

@router.get("/me/experience", response_model=list[ExperienceResponse])
def get_my_experience(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    experiences = db.query(Experience).filter(
        Experience.user_id == current_user.id
    ).all()

    return experiences

@router.put("/me/experience/{experience_id}", response_model=ExperienceResponse)
def update_experience(
    experience_id: int,
    experience: ExperienceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_experience = db.query(Experience).filter(
        Experience.id == experience_id,
        Experience.user_id == current_user.id
    ).first()

    if not existing_experience:
        raise HTTPException(
            status_code=404,
            detail="Experience not found"
        )

    existing_experience.job_title = experience.job_title
    existing_experience.company = experience.company
    existing_experience.description = experience.description
    existing_experience.start_date = experience.start_date
    existing_experience.end_date = experience.end_date

    db.commit()
    db.refresh(existing_experience)

    return existing_experience

@router.delete("/me/experience/{experience_id}")
def delete_experience(
    experience_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_experience = db.query(Experience).filter(
        Experience.id == experience_id,
        Experience.user_id == current_user.id
    ).first()

    if not existing_experience:
        raise HTTPException(
            status_code=404,
            detail="Experience not found"
        )

    db.delete(existing_experience)
    db.commit()

    return {
        "message": "Experience deleted successfully"
    }

