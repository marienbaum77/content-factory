import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from config import settings
from parser import fetch_text_from_url

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    # 1. Запускаем Consumer (Читатель)
    consumer = AIOKafkaConsumer(
        settings.topic_source,
        bootstrap_servers=settings.kafka_broker,
        group_id="content_processor_group", # Важно: имя группы, чтобы помнить, где остановились
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    await consumer.start()

    # 2. Запускаем Producer (Писатель - чтобы отправлять результат дальше)
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker)
    await producer.start()

    logger.info("Processor started. Waiting for messages...")

    try:
        # Бесконечный цикл чтения сообщений
        async for msg in consumer:
            data = msg.value
            url = data.get("link")
            title = data.get("title")
            
            logger.info(f"Processing: {title}")
            
            # Скачиваем текст
            full_text = await fetch_text_from_url(url)
            
            if not full_text:
                continue

            # (Тут позже будет AI). Пока делаем заглушку
            summary = f"Summary заглушка для: {title}. Длина текста: {len(full_text)} символов."
            
            # Формируем результат
            result_message = {
                "original_url": url,
                "title": title,
                "summary": summary,
                "full_text_preview": full_text[:200]
            }

            # Отправляем в топик content.ready
            await producer.send_and_wait(
                settings.topic_result, 
                json.dumps(result_message).encode("utf-8")
            )
            logger.info(f"Done! Sent summary to {settings.topic_result}")

    finally:
        await consumer.stop()
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(main())