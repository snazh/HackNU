from fastapi import APIRouter, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import UserRole
from src.api_v1.auth.dependencies import get_current_user, require_role
from src.database.db import get_async_session
from src.api_v1.users.service import UserService
from src.api_v1.users.dependencies import get_user_service
from src.api_v1.users.schemas import UserCreateSchema, UserUpdateSchema
from src.api_v1.auth.schemas import UserPayloadSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
        service: UserService = Depends(get_user_service),
):
    user = await service.get_by_id(item_id=user_id, session=session)
    return {"status": "Success", "msg": "User fetched", "data": user}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(_: None = require_role(UserRole.admin),
                        session: AsyncSession = Depends(get_async_session),
                        service: UserService = Depends(get_user_service)):
    users = await service.get_all(session=session)
    return {"status": "Success", "msg": "User fetched", "data": users}


@router.post("/", status_code=status.HTTP_200_OK)
async def create_user(user_data: UserCreateSchema,
                      _: None = require_role(UserRole.admin),
                      session: AsyncSession = Depends(get_async_session),
                      service: UserService = Depends(get_user_service)):
    new_user = await service.create(item_data=user_data, session=session)

    return {"status": "Success", "msg": "User created", "data": new_user}


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int,
                      user_data: UserUpdateSchema,
                      user: UserPayloadSchema = Depends(get_current_user),
                      _: None = require_role(UserRole.admin, UserRole.user),
                      session: AsyncSession = Depends(get_async_session),
                      service: UserService = Depends(get_user_service)):
    await service.update_user(user_id=user_id, user_data=user_data, current_user_payload=user, session=session)

    return {"status": "Success", "msg": "User updated"}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      user: UserPayloadSchema = Depends(get_current_user),
                      _: None = require_role(UserRole.admin, UserRole.user),
                      session: AsyncSession = Depends(get_async_session),
                      service: UserService = Depends(get_user_service)):
    await service.delete_user(user_id=user_id, current_user_payload=user, session=session)
