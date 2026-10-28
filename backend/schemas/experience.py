from pydantic import BaseModel, ConfigDict
from datetime import date


class ExperienceCreate(BaseModel):
    job_title: str
    company: str
    description: str | None = None
    start_date: date
    end_date: date | None = None


class ExperienceUpdate(BaseModel):
    job_title: str
    company: str
    description: str | None = None
    start_date: date
    end_date: date | None = None


class ExperienceResponse(BaseModel):
    id: int
    user_id: int
    job_title: str
    company: str
    description: str | None = None
    start_date: date
    end_date: date | None = None

    model_config = ConfigDict(from_attributes=True)