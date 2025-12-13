from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .db import async_session
from .models import ProcessedUrl

class UrlRepository:
    async def is_processed(self, url: str) -> bool:
        """Проверяет, есть ли ссылка в базе"""
        async with async_session() as session:
            # SELECT 1 FROM processed_urls WHERE url = ...
            query = select(ProcessedUrl).where(ProcessedUrl.url == url)
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None

    async def add(self, url: str, source: str):
        """Сохраняет ссылку"""
        async with async_session() as session:
            try:
                new_entry = ProcessedUrl(url=url, source=source)
                session.add(new_entry)
                await session.commit()
            except IntegrityError:
                # Если вдруг гонка потоков и ссылка уже есть
                await session.rollback()