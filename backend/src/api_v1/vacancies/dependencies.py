
from .service import VacancyService, VacancyApplicationService


def get_vacancy_service()->VacancyService:
    return VacancyService()

def get_vacancy_application_service() ->VacancyApplicationService:
    return VacancyApplicationService()