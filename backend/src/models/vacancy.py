from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from .base import Base
from src.models.user import User
import enum


class VacancyStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    PAUSED = "paused"


class EducationLevel(str, enum.Enum):
    HIGH_SCHOOL = "high_school"
    BACHELOR = "bachelor"
    MASTER = "master"
    PHD = "phd"
    ANY = "any"

class EmploymentForm(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    REMOTE = "remote"
class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    company = Column(String(100), nullable=False)
    location = Column(String(100), nullable=True)
    salary = Column(String(50), nullable=True)
    status = Column(Enum(VacancyStatus), default=VacancyStatus.OPEN)
    skills = Column(ARRAY(String), nullable=True)
    education = Column(Enum(EducationLevel), default=EducationLevel.ANY)
    employment_form = Column(Enum(EmploymentForm), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hr_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    hr = relationship("User", back_populates="vacancies")
    applications = relationship("VacancyApplication", back_populates="vacancy")

class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class VacancyApplication(Base):
    __tablename__ = "vacancy_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"), nullable=False)
    message = Column(Text, nullable=True)  # можно оставить сопроводительное сообщение
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="applications")
    vacancy = relationship("Vacancy", back_populates="applications")