from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "OAuth Data Ingestion Demo"
    ENV: str = "development"
    MOCK_OAUTH_CLIENT_ID: str = "mock-client-id"
    MOCK_OAUTH_CLIENT_SECRET: str = "mock-client-secret"
    STORAGE_PATH: str = "mock_s3_data"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
