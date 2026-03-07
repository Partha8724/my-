from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'WhaleScope API'
    environment: str = 'development'
    demo_mode: bool = True

    secret_key: str = 'change-me'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60 * 24

    admin_username: str = 'admin'
    admin_password: str = 'admin123'

    database_url: str = 'sqlite:///./whalescope.db'
    redis_url: str = 'redis://redis:6379/0'
    cors_origins: str = 'http://localhost:3000'

    websocket_poll_seconds: int = 5
    whale_trade_threshold: float = 500000.0
    volume_multiplier_threshold: float = 2.0
    confidence_cutoff: int = 60


settings = Settings()
