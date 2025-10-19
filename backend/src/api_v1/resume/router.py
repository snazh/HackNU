from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.api_v1.auth.dependencies import get_current_user, require_role
from src.database.db import get_async_session
from .schemas import ResumeCreateSchema, ResumeUpdateSchema, ResumeModelSchema
from .dependencies import get_resume_service
from .service import ResumeService
from src.api_v1.auth.dependencies import get_current_user
from src.api_v1.auth.schemas import UserPayloadSchema
from src.models.user import UserRole
router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_resumes(
        _: None = require_role(UserRole.admin),
        session: AsyncSession = Depends(get_async_session),
        service: ResumeService = Depends(get_resume_service)
):
    resumes = await service.get_all(session=session)
    return {"status": "Success", "data": resumes}


@router.get("/my-resume", status_code=status.HTTP_200_OK)
async def get_resume(
        session: AsyncSession = Depends(get_async_session),
        service: ResumeService = Depends(get_resume_service),
        user: UserPayloadSchema = Depends(get_current_user)
):
    resume = await service.get_one_by(field="user_id", value=user.user_id, session=session)

    return {"status": "Success", "data": resume}


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: int,
                        _: None = require_role(UserRole.admin),
                        service: ResumeService = Depends(get_resume_service),
                        session: AsyncSession = Depends(get_async_session)):
    service.delete(session=session, item_id=resume_id)
