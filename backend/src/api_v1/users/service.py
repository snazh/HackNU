from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User, UserRole

from src.api_v1.auth.schemas import UserPayloadSchema
from src.api_v1.auth.utils import password_util
from src.api_v1.common.base_service import BaseService
from src.api_v1.common.base_types import ModelType
from src.api_v1.users.schemas import UserModelSchema, UserCreateSchema, UserUpdateSchema
from src.api_v1.common.errors import ItemNotFoundError, ItemAlreadyExistsError
from src.api_v1.auth.errors import AccessForbiddenError


class UserService(BaseService[User, UserModelSchema]):
    def __init__(self):
        super().__init__(User, UserModelSchema)
        self.password_util = password_util

    async def create_user(self, user_data: UserCreateSchema,

                          session: AsyncSession):

        user_by_email = self.get_one_by(field="email", value=user_data.email, session=session)
        if user_by_email is not None:
            raise ItemAlreadyExistsError(item="user", attr="email", value=user_data.email)

        hashed_password = self.password_util.hash_password(user_data.password)
        user_data.password = hashed_password
        return await super().create(item_data=user_data, session=session)

    async def update_user(self, user_id: int,
                          user_data: UserUpdateSchema,
                          current_user_payload: UserPayloadSchema,
                          session: AsyncSession) -> None:
        await self.check_ownership(user_payload=current_user_payload, resource_user_id=user_id)
        if user_data.role and current_user_payload.role != UserRole.admin.value:
            raise AccessForbiddenError()
        await super().update(item_id=user_id, item_update_data=user_data, session=session)

    async def delete_user(self, user_id: int,
                          current_user_payload: UserPayloadSchema,
                          session: AsyncSession) -> None:
        await self.check_ownership(user_payload=current_user_payload, resource_user_id=user_id)
        await super().delete(item_id=user_id, session=session)
