from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pydantic import PostgresDsn


class BotConfig(BaseModel):
    token: str
    properties: DefaultBotProperties = DefaultBotProperties(parse_mode=ParseMode.HTML)


class Secrets(BaseModel):
    id: str
    secret: str


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    bot: BotConfig
    secrets: Secrets
    db: DatabaseConfig


settings = Settings()
