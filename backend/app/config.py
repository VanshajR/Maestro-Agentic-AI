from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "Agentic AI Automator"
    GROQ_API_KEY: str | None = None
    GROQ_MODELS: list[str] = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gpt-oss-20b",
    ]
    HF_API_KEY: str | None = None
    GITHUB_TOKEN: str | None = None
    SERP_API_KEY: str | None = None
    API_AUTH_KEY: str | None = None
    RATE_LIMIT_PER_MINUTE: int = 60
    CORS_ORIGINS: list[str] = ["*"]
    LOG_LEVEL: str = "INFO"

settings = Settings()
