from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    kafka_broker: str = "localhost:9092"
    topic_source: str = "urls.fetched"  # Отсюда читаем
    topic_result: str = "content.ready" # Сюда пишем
    
    # Фейковый User-Agent, чтобы сайты не думали, что мы бот
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

settings = Settings()