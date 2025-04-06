from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis
from sqlalchemy import URL


class SQLiteSettings(BaseSettings):
    db: str


class RedisSettings(BaseSettings):
    host: str
    port: int
    db: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict()
    developer_id: int
    dev: bool
    bot_token: SecretStr

    psql: SQLiteSettings = SQLiteSettings(_env_prefix="SQLITE_")
    redis: RedisSettings = RedisSettings(_env_prefix="REDIS_")

    def sqlite_dsn(self) -> URL:
        return URL.create(
            drivername="sqlite+aiosqlite",
            database=self.psql.db,
        )

    async def redis_dsn(self) -> Redis:
        return Redis(host=self.redis.host, port=self.redis.port, db=self.redis.db)
