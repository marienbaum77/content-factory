import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer
from aiogram import Bot
from aiogram.enums import ParseMode
from config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def send_to_telegram(bot: Bot, data: dict):
    title = data.get("title", "No Title")
    summary = data.get("summary", "No Summary")
    link = data.get("original_url", "#")
    
    text = (
        f"<b>{title}</b>\n\n"
        f"{summary}\n\n"
        f"👉 <a href='{link}'>Читать оригинал</a>"
    )
    
    try:
        # ИСПРАВЛЕНИЕ 1: settings.tg_chat_id (было telegram_chat_id)
        await bot.send_message(
            chat_id=settings.tg_chat_id, 
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        logger.info(f"Sent to Telegram: {title}")
    except Exception as e:
        logger.error(f"Telegram error: {e}")

async def main():
    # ИСПРАВЛЕНИЕ 2: settings.tg_bot_token (было telegram_bot_token)
    bot = Bot(token=settings.tg_bot_token)
    
    consumer = AIOKafkaConsumer(
        settings.topic_source,
        bootstrap_servers=settings.kafka_broker,
        group_id="telegram_publisher_group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    await consumer.start()
    logger.info("Publisher started. Waiting for content...")

    try:
        async for msg in consumer:
            data = msg.value
            logger.info(f"Received content: {data.get('title')}")
            await send_to_telegram(bot, data)
            
    finally:
        await consumer.stop()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())