from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    kafka_broker: str
    topic_source: str = "urls.fetched"
    topic_result: str = "content.ready"
    
    # Новый ключ
    openrouter_api_key: str
    api_delay: float = 2.0
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()