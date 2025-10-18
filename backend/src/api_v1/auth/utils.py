from datetime import timedelta, datetime
from typing import Literal, Optional

from passlib.context import CryptContext

from src.config import settings

from jose import jwt, ExpiredSignatureError, JWTError
from src.api_v1.auth.errors import InvalidTokenError
from src.api_v1.auth.schemas import UserPayloadSchema


class PasswordUtil:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)


class JwtUtil:
    def __init__(self, secret_key: str, access_token_exp_min: int, refresh_token_exp_min: int, algorithm: str):
        self.secret_key = secret_key
        self.access_token_expire = timedelta(minutes=access_token_exp_min)
        self.refresh_token_expire = timedelta(minutes=refresh_token_exp_min)
        self.algorithm = algorithm

    def create_token(self, data: dict, token_type: Literal["access", "refresh"]) -> Optional[str]:

        if token_type == "access":
            expire = datetime.utcnow() + self.access_token_expire
        elif token_type == "refresh":
            expire = datetime.utcnow() + self.refresh_token_expire

        else:
            # logger.warning("No such type of token")
            return None
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> UserPayloadSchema:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return UserPayloadSchema(**payload)
        except JWTError:
            raise InvalidTokenError()


password_util = PasswordUtil()
jwt_util = JwtUtil(secret_key=settings.auth.AUTH_SECRET, algorithm=settings.auth.AUTH_ALGO,
                   refresh_token_exp_min=settings.auth.REFRESH_TOKEN_EXPIRES_MINUTES,
                   access_token_exp_min=settings.auth.ACCESS_TOKEN_EXPIRES_MINUTES)
