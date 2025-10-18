from src.api_v1.users.service import UserService


def get_user_service() -> UserService:
    return UserService()
