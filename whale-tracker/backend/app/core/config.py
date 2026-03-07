from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "WhaleScope"
    env: str = Field(default="dev")
    debug: bool = True
    log_level: str = "INFO"

    secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 12

    database_url: str = "postgresql+psycopg2://whalescope:whalescope@db:5432/whalescope"
    redis_url: str = "redis://redis:6379/0"

    admin_username: str = "admin"
    admin_password: str = "admin123"

    demo_mode: bool = True
    ws_poll_interval_seconds: int = 3
    whale_trade_threshold_usd: float = 200000
    volume_multiplier_threshold: float = 2.2
    confidence_cutoff: int = 55
    symbol_cooldown_seconds: int = 90
    duplicate_suppression_seconds: int = 120
    confirmation_window_seconds: int = 45
    confirmation_hits: int = 2
    min_volatility_ratio: float = 0.0008
    cors_origins: str = "http://localhost:3000"

    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    smtp_host: str | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("env")
    @classmethod
    def validate_env(cls, value: str) -> str:
        allowed = {"dev", "staging", "prod", "test"}
        if value not in allowed:
            raise ValueError(f"env must be one of {sorted(allowed)}")
        return value

    @model_validator(mode="after")
    def validate_production_requirements(self):
        if self.env == "prod":
            if self.debug:
                raise ValueError("DEBUG must be false in prod")
            if self.secret_key == "change-me":
                raise ValueError("SECRET_KEY must be changed in prod")
        return self


settings = Settings()
