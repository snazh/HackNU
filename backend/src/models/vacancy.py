# from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime
#
# from src.database import Base
#
#
# class Vacancy(Base):
#     title = Column(String(255), nullable=False)
#     description = Column(Text, nullable=False)
#     company_name = Column(String(255), nullable=False)
#     location = Column(String(255), nullable=True)
#     salary = Column(Float, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
#     user = relationship("User", back_populates="vacancies")
#
#
# class VacancyResponse(Base):
