from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str

    algorithm: str
    secret_key: str

    @property
    def async_db_url(self) -> str:
        """Database connection string for async functions."""
        return self.db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    @property
    def sync_db_url(self) -> str:
        """Database connection string for alembic migrations."""
        return self.db_url.replace(
            "postgresql://", "postgresql+psycopg2://", 1
        )

    class Config:
        env_file = ".env"
        extra = "ignore"
        from_attributes = True


settings = Settings()
