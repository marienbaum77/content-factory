from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # === Инфраструктура ===
    # Это значение Pydantic сам найдет в .env по имени KAFKA_BROKER
    kafka_broker: str 
    
    kafka_topic: str = "urls.fetched"

    # === Настройки приложения ===
    # Значения по умолчанию. 
    # Если захочешь сменить источник новостей, просто добавь RSS_URL=... в .env,
    # не меняя этот код.
    rss_url: str = "https://habr.com/ru/rss/articles/?fl=ru"
    poll_interval: int = 60

    # === Конфигурация Pydantic ===
    # env_file=".env" говорит искать файл в корне, откуда ты запускаешь python
    # extra="ignore" позволяет игнорировать лишние переменные в .env 
    # (например, токены от Телеграма, которые нужны Паблишеру, но не нужны Коллектору)
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()