from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "development"
    port: int = 8000
    database_url: str = "postgresql+psycopg://aegis:aegis@localhost:5432/aegis_dev"
    jwt_secret_key: str = "replace-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "anthropic/claude-sonnet-4.5"
    openrouter_temperature: float = 0.2
    openrouter_http_referer: str = "http://localhost:5173"
    openrouter_app_title: str = "Project-Aegis"
    ai_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    gemini_api_key: str = ""
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    gemini_model: str = "gemini-2.0-flash"
    upload_tmp_dir: str = "/tmp/aegis-uploads"
    max_upload_size_mb: int = 200

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
