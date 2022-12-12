import os
from logging import config as logging_config

from pydantic import BaseSettings
from pydantic.fields import Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field(..., env="PROJECT_NAME")
    project_host: str = Field(..., env="PROJECT_HOST")
    project_port: str = Field(..., env="PROJECT_PORT")
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: str = Field(..., env="REDIS_PORT")
    elastic_host: str = Field(..., env="ELASTIC_HOST")
    elastic_port: str = Field(..., env="ELASTIC_PORT")
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache_expire_in_seconds: int = Field(..., env="CACHE_EXPIRE")

    class Config:
        env_file = '.env'


settings = Settings()
