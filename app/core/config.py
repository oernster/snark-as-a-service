from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Monday's Sarcasm API"
    api_version: str = "v1"

    class Config:
        env_file = ".env"


settings = Settings()
