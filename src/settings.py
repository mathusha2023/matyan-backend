from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    host: str
    port: int
    debug: bool

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_database: str

    keycloak_url: str
    keycloak_client: str
    keycloak_secret: str
    keycloak_realm: str
    keycloak_redirect_url: str

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg:"
            f"//{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_database}"
        )


settings = Settings()
