from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from . import constants


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='allow')

    LISTEN_SQL_QUERIES: bool = True
    DEBUG: bool = True

    # Postgres
    POSTGRES_DIALECT: str = 'postgresql+asyncpg'
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def postgres_connection_string(self) -> str:
        user_pwd = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        host_port = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}'
        connection_string = f'{self.POSTGRES_DIALECT}://{user_pwd}@{host_port}/{self.POSTGRES_DB}'
        return connection_string

    @property
    def app_config(self) -> dict[str, Any]:
        conf = {}
        conf['debug'] = self.DEBUG
        conf['description'] = constants.APP_DESCRIPTION
        conf['title'] = constants.APP_TITLE
        return conf


config = Config()
