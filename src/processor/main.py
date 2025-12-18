import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

# Импортируем локальные модули
from config import settings
from parser import fetch_text_from_url
from summarizer import TextSummarizer 

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    # Инициализируем суммаризатор (наш AI-модуль, который генерирует 3 главных предложения)
    ai_model = TextSummarizer()
    
    # 1. Инициализация Consumer (Читает из urls.fetched)
    consumer = AIOKafkaConsumer(
        settings.topic_source,
        bootstrap_servers=settings.kafka_broker,
        group_id="content_processor_group", # Группа для отслеживания прогресса
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="earliest",
        # === НАСТРОЙКИ ДЛЯ МЕДЛЕННОЙ ОБРАБОТКИ (ВАЖНО!) ===
        # 1. Берем только 1 сообщение за раз. 
        # Если взять 10 сообщений и каждое обрабатывать 15 сек,
        # то на 10-м сообщении пройдет 150 сек, и Кафка нас выгонит.
        max_poll_records=1,

        # 2. Увеличиваем тайм-аут сессии до 2 минут (120000 мс).
        # Если мы не шлем хартбиты 2 минуты - тогда считай нас мертвыми.
        session_timeout_ms=120000,

        # 3. Шлем хартбиты каждые 10 секунд (должно быть < 1/3 от session_timeout)
        heartbeat_interval_ms=10000
    )
    await consumer.start()

    # 2. Инициализация Producer (Пишет в content.ready)
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_broker)
    await producer.start()

    logger.info("Processor started (with NLP AI). Waiting for messages...")

    try:
        # Основной цикл обработки сообщений
        async for msg in consumer:
            data = msg.value
            url = data.get("link")
            title = data.get("title")
            
            logger.info(f"Processing: {title}")
            
            # 1. Скачиваем и чистим полный текст статьи (async HTTP call)
            full_text = await fetch_text_from_url(url)
            
            if not full_text:
                logger.warning(f"Empty text for {url}, skipping...")
                continue

            # 2. === ГЕНЕРАЦИЯ SAMMARY (NLP) ===
            logger.info("Summarizing text...")
            try:
                summary = await ai_model.summarize(full_text)
            except Exception as e:
                logger.error(f"Error summarizing text for {title}: {e}")
                # Если AI упал, используем начало текста как резерв
                summary = f"Краткое описание недоступно: {full_text[:300]}..." 
            # =================================

            # 3. Формируем финальное сообщение для публикации
            result_message = {
                "original_url": url,
                "title": title,
                "summary": summary, 
            }

            # 4. Отправляем в следующий топик
            await producer.send_and_wait(
                settings.topic_result, 
                json.dumps(result_message).encode("utf-8")
            )
            logger.info(f"Successfully processed and sent: {title}")
            await asyncio.sleep(settings.api_delay) 
    except asyncio.CancelledError:
        logger.info("Processor was cancelled.")
    finally:
        await consumer.stop()
        await producer.stop()
        logger.info("Processor stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service stopped manually")