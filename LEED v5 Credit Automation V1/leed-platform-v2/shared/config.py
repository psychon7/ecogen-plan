"""Configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration — sourced from env vars / .env file."""

    # Database
    database_url: str = "postgresql+asyncpg://leed:leed_secret@localhost:5432/leed_platform"

    # Restate
    restate_admin_url: str = "http://localhost:9070"
    restate_ingress_url: str = "http://localhost:8080"

    # S3 / MinIO
    s3_endpoint_url: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket_evidence: str = "leed-evidence"
    s3_bucket_documents: str = "leed-documents"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    openai_extraction_model: str = "gpt-4o"

    # Auth
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440

    # App
    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
