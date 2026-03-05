from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Whale Tracker"
    environment: str = "dev"
    database_url: str = "sqlite:///./whale_tracker.db"
    poll_interval_seconds: int = 30

    # Providers
    crypto_provider: str = "mock"
    stock_provider: str = "mock"
    xau_provider: str = "mock"
    whale_alert_api_key: str | None = None
    etherscan_api_key: str | None = None
    alpaca_api_key: str | None = None
    alpaca_secret_key: str | None = None
    twelvedata_api_key: str | None = None

    # Notifications
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    email_from: str | None = None
    email_to: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
