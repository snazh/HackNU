from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models.vacancy import Vacancy, EducationLevel, VacancyApplication, VacancyStatus
from sqlalchemy import delete, inspect, select, update
from src.api_v1.auth.schemas import UserPayloadSchema
from src.api_v1.auth.utils import password_util
from src.api_v1.common.base_service import BaseService
from src.api_v1.common.base_types import ModelType
from src.api_v1.users.schemas import UserModelSchema, UserCreateSchema, UserUpdateSchema
from src.api_v1.common.errors import ItemNotFoundError, ItemAlreadyExistsError
from src.api_v1.auth.errors import AccessForbiddenError
from src.api_v1.vacancies.schemas import VacancyCreateSchema, VacancyUpdateSchema, VacancyModelSchema, \
    VacancyApplicationCreateSchema, VacancyApplicationModelSchema
from src.models.resume import Resume


class VacancyService(BaseService[Vacancy, VacancyModelSchema]):
    def __init__(self):
        super().__init__(Vacancy, VacancyModelSchema)

    async def create_vacancy(self, vacancy_data: VacancyCreateSchema, session: AsyncSession):
        return await super().create(item_data=vacancy_data, session=session)

    async def update_vacancy(self, vacancy_id: int,
                             vacancy_data: VacancyUpdateSchema,
                             current_user_payload: UserPayloadSchema,
                             session: AsyncSession) -> None:
        existing_vacancy = await self.get_one_by(session=session, field="id", value=vacancy_id)
        await self.check_ownership(user_payload=current_user_payload, resource_user_id=existing_vacancy.id)

        await super().update(item_id=existing_vacancy.id, item_update_data=vacancy_data, session=session)

    async def delete_vacancy(self, vacancy_id: int,
                             current_user_payload: UserPayloadSchema,
                             session: AsyncSession) -> None:
        existing_vacancy = await self.get_one_by(session=session, field="id", value=vacancy_id)
        await self.check_ownership(user_payload=current_user_payload, resource_user_id=existing_vacancy.id)
        await super().delete(item_id=vacancy_id, session=session)

    async def change_status(self, vacancy_id: int,
                            new_status: VacancyStatus,
                            current_user_payload: UserPayloadSchema,
                            session: AsyncSession) -> None:
        existing_vacancy = await self.get_one_by(session=session, field="id", value=vacancy_id)
        await self.check_ownership(user_payload=current_user_payload, resource_user_id=existing_vacancy.id)
        vacancy_data = VacancyUpdateSchema(status=new_status)
        await super().partial_update(item_id=vacancy_id, item_update_data=vacancy_data, session=session)


class VacancyApplicationService(BaseService[VacancyApplication, VacancyApplicationModelSchema]):
    def __init__(self):
        super().__init__(VacancyApplication, VacancyApplicationModelSchema)

    async def apply(self, application_data: VacancyApplicationCreateSchema, session: AsyncSession):
        new_application = await super().create(item_data=application_data, session=session)
        stmt = select(Resume).where(Resume.user_id == new_application.user_id)
        result = await session.execute(stmt)
        resume = result.scalar_one_or_none()
        return {"application": new_application, "resume": resume}
    async def get_applied_resumes(self, vacancy_id: int, session: AsyncSession):
        stmt = (
            select(Resume)
            .join(Resume.user)  # через relationship user
            .join(VacancyApplication, VacancyApplication.user_id == Resume.user_id)
            .where(VacancyApplication.vacancy_id == vacancy_id)
        )
        result = await session.execute(stmt)
        resumes = result.scalars().all()
        return resumes

