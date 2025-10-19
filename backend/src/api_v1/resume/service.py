from sqlalchemy.ext.asyncio import AsyncSession
from src.api_v1.common.base_service import BaseService
from src.api_v1.common.errors import ItemNotFoundError
from src.models.resume import Resume
from src.models.vacancy import VacancyApplication, Vacancy
from .schemas import ResumeModelSchema, ResumeCreateSchema, ResumeUpdateSchema


class ResumeService(BaseService[Resume, ResumeModelSchema]):
    def __init__(self):
        super().__init__(Resume, ResumeModelSchema)
