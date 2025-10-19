from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.resume import Resume
from src.models.vacancy import EducationLevel, EmploymentForm
from src.models.user import UserRole
from src.api_v1.auth.dependencies import get_current_user, require_role
from src.database.db import get_async_session
from src.api_v1.auth.schemas import UserPayloadSchema
from src.api_v1.common.errors import ItemNotFoundError, ItemAlreadyExistsError
from src.api_v1.vacancies.errors import VacancyClosedError
from src.models.vacancy import VacancyStatus
from src.api_v1.vacancies.service import VacancyService, VacancyApplicationService
from src.api_v1.vacancies.dependencies import get_vacancy_service, get_vacancy_application_service
from src.api_v1.vacancies.schemas import VacancyCreateSchema, VacancyUpdateSchema, VacancyApplicationCreateSchema
from .llm_service import analyze_resume

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@router.get("/{vacancy_id}", status_code=status.HTTP_200_OK)
async def get_vacancy(
        vacancy_id: int,
        session: AsyncSession = Depends(get_async_session),
        service: VacancyService = Depends(get_vacancy_service),
):
    vacancy = await service.get_by_id(item_id=vacancy_id, session=session)
    return {"status": "Success", "msg": "Vacancy fetched", "data": vacancy}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_vacancies(
        user: UserPayloadSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
        service: VacancyService = Depends(get_vacancy_service)):
    vacancies = await service.get_all_vacancies(session=session, user_id=user.user_id)
    return {"status": "Success", "msg": "Vacancy fetched", "data": vacancies}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vacancy(vacancy_data: VacancyCreateSchema,
                         user: UserPayloadSchema = Depends(get_current_user),
                         _: None = require_role(UserRole.admin, UserRole.hr),
                         session: AsyncSession = Depends(get_async_session),
                         service: VacancyService = Depends(get_vacancy_service)):
    vacancy_data.hr_id = user.user_id
    new_vacancy = await service.create(item_data=vacancy_data, session=session)

    return {"status": "Success", "msg": "Vacancy created", "data": new_vacancy}


@router.put("/{vacancy_id}", status_code=status.HTTP_200_OK)
async def update_vacancy(vacancy_id: int,
                         vacancy_data: VacancyUpdateSchema,
                         user: UserPayloadSchema = Depends(get_current_user),
                         _: None = require_role(UserRole.admin, UserRole.hr),
                         session: AsyncSession = Depends(get_async_session),
                         service: VacancyService = Depends(get_vacancy_service)):
    await service.update_vacancy(vacancy_id=vacancy_id, vacancy_data=vacancy_data, current_user_payload=user,
                                 session=session)

    return {"status": "Success", "msg": "Vacancy updated"}


@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy(vacancy_id: int,
                         user: UserPayloadSchema = Depends(get_current_user),
                         _: None = require_role(UserRole.admin, UserRole.hr),
                         session: AsyncSession = Depends(get_async_session),
                         service: VacancyService = Depends(get_vacancy_service)):
    await service.delete_vacancy(vacancy_id=vacancy_id, current_user_payload=user, session=session)


@router.post("/{vacancy_id}/change-status", status_code=status.HTTP_200_OK)
async def change_status(vacancy_id: int,
                        new_status: VacancyStatus,
                        user: UserPayloadSchema = Depends(get_current_user),
                        _: None = require_role(UserRole.admin, UserRole.hr),
                        session: AsyncSession = Depends(get_async_session),
                        service: VacancyService = Depends(get_vacancy_service)):
    await service.change_status(vacancy_id=vacancy_id, current_user_payload=user, new_status=new_status,
                                session=session)
    return {"status": "Success", "msg": "Vacancy status changed"}


@router.post("/{vacancy_id}/apply", status_code=status.HTTP_201_CREATED)
async def apply_to_vacancy(
        vacancy_id: int,
        user: UserPayloadSchema = Depends(get_current_user),
        _: None = require_role(UserRole.admin, UserRole.user),
        session: AsyncSession = Depends(get_async_session),
        service: VacancyApplicationService = Depends(get_vacancy_application_service),
        vacancy_service: VacancyService = Depends(get_vacancy_service)):
    vacancy = await vacancy_service.get_by_id(item_id=vacancy_id, session=session)
    if vacancy is None:
        raise ItemNotFoundError(item="vacancy", attr="id", value=vacancy_id)
    if vacancy.status != VacancyStatus.OPEN:
        raise VacancyClosedError()

    application_data = VacancyApplicationCreateSchema(user_id=user.user_id, vacancy_id=vacancy_id)
    applicant_resume = await service.apply(application_data=application_data, session=session)
    decision = analyze_resume(resume=applicant_resume, vacancy=vacancy)
    return {"status": "Success", "msg": "Application sent", "data": decision}


@router.get("/{vacancy_id}/applications", status_code=status.HTTP_200_OK)
async def get_applied_resumes(vacancy_id: int,
                              user: UserPayloadSchema = Depends(get_current_user),
                              _: None = require_role(UserRole.admin, UserRole.user),
                              session: AsyncSession = Depends(get_async_session),
                              service: VacancyApplicationService = Depends(get_vacancy_application_service),
                              vacancy_service: VacancyService = Depends(get_vacancy_service)):
    existing_vacancy = await vacancy_service.get_one_by(
        session=session,
        field="id",
        value=vacancy_id
    )
    if not existing_vacancy:
        raise ItemNotFoundError(item="vacancy", attr="vacancy_id", value=vacancy_id)
    resumes = await service.get_applied_resumes(vacancy_id=vacancy_id, session=session)
    return {"status": "Success", "msg": "Applied resume fetched", "data": resumes}


@router.post("/create-user1", status_code=status.HTTP_201_CREATED)
async def create_resume_user1(session: AsyncSession = Depends(get_async_session)):
    # создаём резюме для пользователя с id=1
    resume = Resume(
        user_id=1,
        title="Junior Python Developer",
        summary="Ищу работу Python-разработчиком.",
        experience=[{"company": "Компания А", "role": "Intern", "years": 1}],
        skills=["Python", "FastAPI", "SQLAlchemy"],
        education=EducationLevel.BACHELOR,
        languages=["Русский", "Английский"],
        location="Нур-Султан",
        salary_expectation="100000 KZT",
        employment_form=EmploymentForm.FULL_TIME,
    )

    session.add(resume)
    await session.commit()
    await session.refresh(resume)

    return {"status": "Success", "msg": "Resume created for user 1", "data": resume}


@router.post("/my-applications")
async def my_applications(
        user: UserPayloadSchema = Depends(get_current_user),
        service: VacancyApplicationService = Depends(get_vacancy_application_service),
        session: AsyncSession = Depends(get_async_session)):
    applications = await service.get_all_by(field="user_id", value=user.user_id, session=session)
    return {"status": "Success", "msg": "MY applications", "data": applications}
