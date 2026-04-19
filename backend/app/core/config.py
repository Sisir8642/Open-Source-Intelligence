from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "OSINT Intelligence Platform"
    DEBUG: bool = True
    SECRET_KEY: str = "changeme"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/osint_db"

    # Real API Keys
    GOOGLE_API_KEY: str = ""
    GOOGLE_CSE_ID: str = ""
    GITHUB_TOKEN: str = ""
    NEWS_API_KEY: str = ""
    WHOIS_API_KEY: str = ""
    HIBP_API_KEY: str = ""
    OPENCORPORATES_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
