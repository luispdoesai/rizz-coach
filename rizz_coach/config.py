from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # LLM Settings
    llm_provider: str = Field(default="mock", alias="LLM_PROVIDER")
    llm_model: str = Field(default="gpt-4o-mini", alias="LLM_MODEL")
    llm_api_key: Optional[str] = Field(default=None, alias="LLM_API_KEY")
    llm_base_url: str = Field(default="https://api.openai.com/v1", alias="LLM_BASE_URL")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")

    # Automation Engine Settings
    automation_mode: str = Field(default="copilot", alias="AUTOMATION_MODE")
    automation_min_delay_seconds: int = Field(default=180, alias="AUTOMATION_MIN_DELAY_SECONDS")
    automation_max_delay_seconds: int = Field(default=720, alias="AUTOMATION_MAX_DELAY_SECONDS")
    alert_on_conversion: bool = Field(default=True, alias="ALERT_ON_CONVERSION")

    # Integrations & Connectors
    telegram_bot_token: Optional[str] = Field(default=None, alias="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = Field(default=None, alias="TELEGRAM_CHAT_ID")
    tinder_auth_token: Optional[str] = Field(default=None, alias="TINDER_AUTH_TOKEN")
    instagram_session_id: Optional[str] = Field(default=None, alias="INSTAGRAM_SESSION_ID")
    max_daily_outreach: int = Field(default=15, alias="MAX_DAILY_OUTREACH")
    twilio_account_sid: Optional[str] = Field(default=None, alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    twilio_phone_number: Optional[str] = Field(default=None, alias="TWILIO_PHONE_NUMBER")

    # Server Settings
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    debug: bool = Field(default=True, alias="DEBUG")
    database_path: str = Field(default="rizz_coach.db", alias="DATABASE_PATH")

settings = Settings()
