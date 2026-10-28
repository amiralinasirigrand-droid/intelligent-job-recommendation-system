from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models.skill import Skill
from schemas.skill import SkillResponse


router = APIRouter(
    prefix="/api/skills",
    tags=["Skills"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[SkillResponse])
def get_all_skills(
    db: Session = Depends(get_db)
):
    skills = db.query(Skill).all()

    return skills