from pydantic import BaseModel, ConfigDict
from datetime import date



class EducationCreate(BaseModel):
    degree: str
    field_of_study: str
    institution: str
    start_date: date | None = None
    end_date: date | None = None

class EducationUpdate(BaseModel):
    degree: str
    field_of_study: str
    institution: str
    start_date: date
    end_date: date | None = None

class EducationResponse(BaseModel):
    id: int
    user_id: int
    degree: str
    field_of_study: str
    institution: str
    start_date: date | None = None
    end_date: date | None = None
    model_config = ConfigDict(from_attributes=True)