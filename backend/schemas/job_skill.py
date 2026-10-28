from pydantic import BaseModel


class JobSkillCreate(BaseModel):
    skill_id: int
    required_level: str | None = None
    is_required: bool = True


class JobSkillResponse(BaseModel):
    job_id: int
    skill_id: int
    required_level: str | None = None
    is_required: bool

class JobSkillDetailResponse(BaseModel):
    job_id: int
    skill_id: int
    skill_name: str
    required_level: str | None = None
    is_required: bool

class JobSkillUpdate(BaseModel):
    required_level: str | None = None
    is_required: bool