from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from src.models.vacancy import VacancyStatus, EducationLevel,ApplicationStatus

class VacancyCreateSchema(BaseModel):
    title: str
    description: str
    company: str
    location: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[VacancyStatus] = VacancyStatus.OPEN
    skills: Optional[List[str]] = []
    education: Optional[EducationLevel] = EducationLevel.ANY
    hr_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class VacancyUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[VacancyStatus] = None
    skills: Optional[List[str]] = None
    education: Optional[EducationLevel] = None
    hr_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class VacancyDTO(VacancyCreateSchema):
    pass


class VacancyModelSchema(VacancyCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

class VacancyApplicationCreateSchema(BaseModel):
    user_id: Optional[int] = None
    vacancy_id: int
    message: Optional[str] = None
    status: Optional[ApplicationStatus] = ApplicationStatus.PENDING

    model_config = ConfigDict(from_attributes=True)


class VacancyApplicationModelSchema(VacancyApplicationCreateSchema):
    id: int
    created_at: datetime
