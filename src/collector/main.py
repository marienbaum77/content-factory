import asyncio
import json
import logging
import feedparser
from aiokafka import AIOKafkaProducer
from config import settings

# Импортируем нашу БД
from storage.db import init_db
from storage.repository import UrlRepository

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker)
    await producer.start()
    return producer

async def main():
    logger.info("Service Collector started...")
    
    # 1. Создаем таблицу в БД (если её нет)
    await init_db()
    
    # 2. Инициализируем репозиторий
    repo = UrlRepository()
    
    producer = await get_kafka_producer()

    try:
        while True:
            logger.info(f"Fetching RSS from {settings.rss_url}")
            feed = feedparser.parse(settings.rss_url)

            for entry in feed.entries:
                link = entry.link
                
                # === ПРОВЕРКА НА ДУБЛИКАТЫ ===
                if await repo.is_processed(link):
                    logger.debug(f"Skipping {link} (already processed)")
                    continue
                # ==============================

                message = {
                    "title": entry.title,
                    "link": link,
                    "published": entry.published
                }

                value_json = json.dumps(message).encode('utf-8')
                await producer.send_and_wait(settings.kafka_topic, value_json)
                
                # === ЗАПОМИНАЕМ ССЫЛКУ ===
                await repo.add(link, source="habr")
                logger.info(f"New article sent: {entry.title}")

            logger.info(f"Sleeping for {settings.poll_interval} seconds...")
            await asyncio.sleep(settings.poll_interval)

    except Exception as e:
        logger.error(f"Critical error: {e}")
    finally:
        await producer.stop()
        logger.info("Producer stopped")

if __name__ == "__main__":
    asyncio.run(main()) 