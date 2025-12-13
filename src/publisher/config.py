from typing import Union
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    kafka_broker: str
    topic_source: str = "content.ready"
    
    tg_bot_token: str
    
    # ИСПРАВЛЕНИЕ 1: Разрешаем и число (для приватных), и строку (для публичных @channel)
    tg_chat_id: Union[int, str]

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        # ИСПРАВЛЕНИЕ 2: Игнорируем DB_HOST, DB_USER и прочее,
        # что лежит в .env, но не нужно Паблишеру
        extra="ignore"
    )

settings = Settings()