# src/models/user.py
from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from enum import Enum as PyEnum


class UserRole(PyEnum):
    admin = "admin"
    user = "user"
    hr = "hr"


class User(Base):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="role", create_constraint=True),
        nullable=False,
        default=UserRole.user
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    vacancies = relationship("Vacancy", back_populates="hr")
    applications = relationship("VacancyApplication", back_populates="user")
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    resume = relationship("Resume", back_populates="user", uselist=False)