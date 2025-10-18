from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from src.api_v1.auth.schemas import RegisterSchema, LoginSchema, TokenSchema
from src.api_v1.common.base_service import BaseService
from src.api_v1.common.base_types import ModelType
from src.api_v1.common.errors import ItemAlreadyExistsError
from src.api_v1.auth.errors import InvalidCredentialsError
from src.api_v1.auth.utils import password_util, jwt_util
from src.config import settings
from src.api_v1.users.schemas import UserModelSchema
from src.models import User


class AuthService(BaseService[User, UserModelSchema]):
    def __init__(self):

        super().__init__(User, UserModelSchema)
        # dictionary for utils
        self.utils = {
            "password": password_util,
            "jwt": jwt_util
        }

    async def register(self, session: AsyncSession, user_data: RegisterSchema):
        existing_user = await self.get_one_by(session=session, field="email", value=user_data.email)

        if existing_user is not None:
            raise ItemAlreadyExistsError(item="user", attr="email", value=user_data.email)

        hashed_password = self.utils["password"].hash_password(user_data.password)
        user_data.password = hashed_password
        return await super().create(item_data=user_data, session=session)

    async def login(self, session: AsyncSession, user_data: LoginSchema):
        user = await self.get_one_by(session=session, field="email", value=user_data.email)
        is_match = self.utils["password"].verify_password(plain_password=user_data.password,
                                                          hashed_password=user.password)

        if not (user and is_match):
            raise InvalidCredentialsError()

        payload = {"user_id": str(user.id), "role": user.role.value}
        return TokenSchema(refresh=self.utils["jwt"].create_token(payload, token_type="access"),
                           access=self.utils["jwt"].create_token(payload, token_type="refresh"))
