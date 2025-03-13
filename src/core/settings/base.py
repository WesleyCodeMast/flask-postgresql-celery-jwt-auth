from pydantic_settings import BaseSettings as BasePydanticSettings, SettingsConfigDict

from dotenv import find_dotenv


class BaseSettings(BasePydanticSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv(), extra='allow')
