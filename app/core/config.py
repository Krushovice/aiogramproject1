from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    BOT_TOKEN: str
    AI_ID: str
    AI_SECRET: str
    DEBUG: bool
    ECHO: bool = False

    @property
    def db_url(self) -> str:
        if self.DEBUG:
            return "sqlite+aiosqlite:///./db.sqlite3"
        else:
            return f"{self.DB_URL}"

    @property
    def bot_token(self) -> str:
        return f"{self.BOT_TOKEN}"

    @property
    def api_token(self) -> str:
        return f"{self.AI_ID}"

    @property
    def ai_secret(self) -> str:
        return f"{self.AI_SECRET}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
