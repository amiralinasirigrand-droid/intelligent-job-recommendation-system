
from sqlalchemy import Column, Integer, ForeignKey, String

from database import Base


class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        primary_key=True
    )

    skill_level = Column(
        String(50),
        nullable=False,
        default="Beginner",
        server_default="Beginner"
    )
