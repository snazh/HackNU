from src.api_v1.common.errors import BaseAppException
from starlette import status


class NotAuthorizedError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Not authorized"
        )


class NotAuthenticatedError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Not authenticated. Please log in"
        )


class InvalidCredentialsError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid credentials"
        )


class AccessForbiddenError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Access Forbidden. Insufficient role"
        )


class TokenExpiredError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Token expired"
        )


class InvalidTokenError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid token"
        )
