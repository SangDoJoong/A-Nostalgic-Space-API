import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str
    SECRET_KEY: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    SWAGGER_NAME: str
    SWAGGER_PASSWORD: str

    class Config:
        env_file = f".env.{os.getenv('APP_ENV', 'local')}"
