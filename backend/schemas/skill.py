
from pydantic import BaseModel, Field


class SkillResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


class UserSkillCreate(BaseModel):
    skill_id: int
    skill_level: str = Field(
        default="Beginner",
        pattern="^(Beginner|Intermediate|Advanced)$"
    )
