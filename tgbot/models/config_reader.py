from pydantic import SecretStr, RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    PG_DSN: PostgresDsn
    REDIS_DSN: RedisDsn
    LOGGING_MODE: str
    ADMIN_CHAT_ID: str

    def debug_status(self):
        return True if self.LOGGING_MODE == "DEBUG" else False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
