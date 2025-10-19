from src.api_v1.common.errors import BaseAppException
from starlette import status


class VacancyClosedError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Vacancy closed"
        )



