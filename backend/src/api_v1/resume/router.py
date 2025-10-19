from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database.db import get_async_session
from .schemas import ResumeCreateSchema, ResumeUpdateSchema, ResumeModelSchema
from .dependencies import get_resume_service
from .service import ResumeService
from src.api_v1.auth.dependencies import get_current_user
from src.api_v1.auth.schemas import UserPayloadSchema

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.get("/", response_model=List[ResumeModelSchema])
async def get_all_resumes(
        session: AsyncSession = Depends(get_async_session),
        service: ResumeService = Depends(get_resume_service)
):
    return await service.get_all(session=session)


@router.get("/{resume_id}", response_model=ResumeModelSchema)
async def get_resume(
        resume_id: int,
        session: AsyncSession = Depends(get_async_session),
        service: ResumeService = Depends(get_resume_service)
):
    return await service.get_by_id(item_id=resume_id, session=session)


@router.post("/", response_model=ResumeModelSchema, status_code=status.HTTP_201_CREATED)
async def create_resume(
        resume_data: ResumeCreateSchema,
        user: UserPayloadSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
        service: ResumeService = Depends(get_resume_service)
):
    resume_data.user_id = user.id
    return await service.create(item_data=resume_data, session=session)


@router.put("/{resume_id}", status_code=status.HTTP_200_OK)
async def update_resume(
        resume_id: int,
        resume_data: ResumeUpdateSchema,
        user: UserPayloadSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
        service: ResumeService = Depends(get_resume_service)
):
    await service.update(item_id=resume_id, item_update_data=resume_data, session=session)
    return {"status": "Success", "msg": "Resume updated"}


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
        resume_id: int,
        user: UserPayloadSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
        service: ResumeService = Depends(get_resume_service)
):
    await service.delete(item_id=resume_id, session=session)
