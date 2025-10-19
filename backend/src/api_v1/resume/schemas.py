from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from src.models.vacancy import EducationLevel

class ResumeCreateSchema(BaseModel):
    title: Optional[str]
    summary: Optional[str]
    experience: Optional[dict]
    skills: Optional[List[str]]
    education: Optional[EducationLevel]

    model_config = ConfigDict(from_attributes=True)

class ResumeUpdateSchema(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    experience: Optional[dict] = None
    skills: Optional[List[str]] = None
    education: Optional[EducationLevel] = None

    model_config = ConfigDict(from_attributes=True)

class ResumeModelSchema(ResumeCreateSchema):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
