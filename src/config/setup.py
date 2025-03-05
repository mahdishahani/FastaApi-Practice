import os
from typing import Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAPI documentation.
    name: Union[str, None] = None
    version: Union[str, None] = None

    # Service parameters.
    service_name: Union[str, None] = None
    service_log_level: Union[str, None] = None

    debug: Union[bool, None] = None
    database_hostname: Union[str, None] = None
    database_port: Union[str, None] = None
    database_username: Union[str, None] = None
    database_password: Union[str, None] = None
    database_name: Union[str, None] = None
    rabbitmq_default_user: Union[str, None] = None
    rabbitmq_default_pass: Union[str, None] = None
    rabbitmq_default_vhost: Union[str, None] = None
    rabbitmq_default_host: Union[str, None] = None
    rabbitmq_default_port: Union[str, None] = None
    rabbit_url: Union[str, None] = None

    class Config:
        env_file = ".env"


settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
