from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from src.models.vacancy import VacancyStatus, EducationLevel, ApplicationStatus, EmploymentForm

# ---------------- Resumes ----------------

class ResumeCreateSchema(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    experience: Optional[List[dict]] = None  # Список словарей с опытом
    skills: Optional[List[str]] = None
    education: Optional[EducationLevel] = None
    languages: Optional[List[str]] = None
    location: Optional[str] = None
    salary_expectation: Optional[str] = None
    employment_form: Optional[EmploymentForm] = None

    model_config = ConfigDict(from_attributes=True)


class ResumeUpdateSchema(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    experience: Optional[List[dict]] = None
    skills: Optional[List[str]] = None
    education: Optional[EducationLevel] = None
    languages: Optional[List[str]] = None
    location: Optional[str] = None
    salary_expectation: Optional[str] = None
    employment_form: Optional[EmploymentForm] = None

    model_config = ConfigDict(from_attributes=True)


class ResumeModelSchema(ResumeCreateSchema):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

# ---------------- Vacancies ----------------

class VacancyCreateSchema(BaseModel):
    title: str
    description: str
    company: str
    location: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[VacancyStatus] = VacancyStatus.OPEN
    skills: Optional[List[str]] = None
    education: Optional[EducationLevel] = EducationLevel.ANY
    hr_id: Optional[int] = None
    employment_form: Optional[EmploymentForm] = None  # ✅ добавлено

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
    employment_form: Optional[EmploymentForm] = None  # ✅ добавлено

    model_config = ConfigDict(from_attributes=True)


class VacancyModelSchema(VacancyCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

# ---------------- Applications ----------------

class VacancyApplicationCreateSchema(BaseModel):
    user_id: Optional[int] = None
    vacancy_id: int
    message: Optional[str] = None
    status: Optional[ApplicationStatus] = ApplicationStatus.PENDING

    model_config = ConfigDict(from_attributes=True)


class VacancyApplicationModelSchema(VacancyApplicationCreateSchema):
    id: int
    created_at: datetime
