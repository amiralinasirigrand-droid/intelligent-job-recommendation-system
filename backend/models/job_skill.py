from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class JobSkill(Base):
    __tablename__ = "job_skills"

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        primary_key=True
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        primary_key=True
    )

    required_level = Column(String(50))
    is_required = Column(Boolean, nullable=False)