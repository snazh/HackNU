from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# declaring path to .env file
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
ENV_PATH = os.path.join(ROOT_DIR, '.env')

TMP_S3_STORAGE_PATH = os.path.join(ROOT_DIR, 'tmp_s3_storage')


class CoreConfig(BaseSettings):
    model_config = SettingsConfigDict(  # configuring .env file
        env_file=ENV_PATH,
        env_file_encoding='utf-8',
        extra="ignore")  # ignoring other secret keys


class DBSettings(CoreConfig):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def async_database_url(self) -> str:
        # Construct the async database URL
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class AuthSettings(CoreConfig):
    AUTH_ALGO: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int
    REFRESH_TOKEN_EXPIRES_MINUTES: int
    AUTH_SECRET: str


class AdminSettings(CoreConfig):
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str


class S3BucketSettings(CoreConfig):
    AWS_BUCKET_NAME: str
    AWS_REGION: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    media_storage: Path = TMP_S3_STORAGE_PATH


class ExternalApiSettings(CoreConfig):
    OPENAI_API_KEY: str


class RedisSetting(CoreConfig):
    REDIS_HOST: str
    REDIS_PORT: int


class Settings(CoreConfig):
    db: DBSettings = DBSettings()
    auth: AuthSettings = AuthSettings()
    admin_data: AdminSettings = AdminSettings()
    s3bucket: S3BucketSettings = S3BucketSettings()
    redis: RedisSetting = RedisSetting()
    external_api: ExternalApiSettings = ExternalApiSettings()


settings = Settings()
