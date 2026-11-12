import logging
import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger("dermasense")
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), extra="ignore")

    env: str = "development"
    mongo_uri: str = "mongodb://localhost:27017"
    database_name: str = "dermasense"
    redis_url: str = ""
    chroma_path: str = str(BASE_DIR / "chroma_storage")
    data_dir: str = str(BASE_DIR / "data")
    ollama_model: str = "llama3"
    ollama_host: str = ""
    embedding_backend: str = "auto"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    rag_min_score: float = 0.2
    whisper_model: str = "base"
    max_audio_mb: int = 15
    jwt_secret: str = ""
    jwt_expire_minutes: int = 480
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.env.lower() == "production"


settings = Settings()
_secret_cache: list[str] = []


def jwt_secret() -> str:
    """Return the signing secret. Production refuses to run without one."""
    if settings.jwt_secret:
        return settings.jwt_secret
    if settings.is_production:
        raise RuntimeError("JWT_SECRET must be set when ENV=production")
    if not _secret_cache:
        _secret_cache.append(secrets.token_urlsafe(48))
        log.warning("JWT_SECRET not set: using a temporary secret. Tokens reset on restart.")
    return _secret_cache[0]
