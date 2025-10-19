from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from .vacancy import EducationLevel
import enum
from src.models.vacancy import EmploymentForm



class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
    experience = Column(JSON, nullable=True)  # JSON
    skills = Column(ARRAY(String), nullable=True)  # массив строк
    education = Column(Enum(EducationLevel), default=EducationLevel.ANY)

    # Новые поля
    languages = Column(ARRAY(String), nullable=True)
    location = Column(String(100), nullable=True)
    salary_expectation = Column(String(50), nullable=True)
    employment_form = Column(Enum(EmploymentForm), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="resumes")
