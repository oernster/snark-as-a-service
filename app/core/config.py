from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "My Sarcasm API"

    # Pydantic v2 style configuration (avoids deprecation warnings in tests)
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
