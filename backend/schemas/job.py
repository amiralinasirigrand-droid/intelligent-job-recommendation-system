from pydantic import BaseModel, ConfigDict
from datetime import datetime
from schemas.job_skill import JobSkillDetailResponse

class JobCreate(BaseModel):
    title: str
    company: str
    description: str | None = None
    location: str | None = None
    employment_type: str | None = None


class JobUpdate(BaseModel):
    title: str
    company: str
    description: str | None = None
    location: str | None = None
    employment_type: str | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    description: str | None = None
    location: str | None = None
    employment_type: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobDetailResponse(JobResponse):
    skills: list["JobSkillDetailResponse"] = []