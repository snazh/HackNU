from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.dependencies import get_auth_service, get_current_user
from src.database.db import get_async_session
from src.api_v1.auth.schemas import RegisterSchema, LoginSchema, UserPayloadSchema
from src.api_v1.auth.service import AuthService
from src.api_v1.common.errors import ItemNotFoundError
from src.config import settings
from src.api_v1.users.schemas import UserModelSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: RegisterSchema,
                   service: AuthService = Depends(get_auth_service),
                   session: AsyncSession = Depends(get_async_session)):
    new_user = await service.register(user_data=user_data, session=session)

    return {"status": "Success", "msg": "User created", "data": new_user}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_data: LoginSchema,
                response: Response,
                service: AuthService = Depends(get_auth_service),
                session: AsyncSession = Depends(get_async_session),
                ):
    tokens = await service.login(user_data=user_data, session=session)
    response.set_cookie(
        key="access_token",
        value=tokens.access,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * settings.auth.ACCESS_TOKEN_EXPIRES_MINUTES,  # 15 minutes
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * settings.auth.REFRESH_TOKEN_EXPIRES_MINUTES,  # 7 days
    )
    user = await service.get_one_by(field="email", value=user_data.email, session=session)
    return {"status": "Success", "msg": "Logged in", "data": {"user":user}}


@router.get("/profile", status_code=status.HTTP_200_OK)
async def get_profile(user: UserPayloadSchema = Depends(get_current_user),
                      session: AsyncSession = Depends(get_async_session),
                      service: AuthService = Depends(get_auth_service)):
    user = await service.get_by_id(item_id=user.user_id, session=session)

    return {"status": "Success", "msg": "Profile fetched", "data": user}
