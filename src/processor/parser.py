import trafilatura
from config import settings

async def fetch_text_from_url(url: str) -> str:
    try:
        # Trafilatura умеет сама скачивать, но лучше скачаем и отдадим ей строку
        downloaded = trafilatura.fetch_url(url)
        
        if downloaded is None:
            return ""

        # include_comments=False убирает комментарии (частый источник мусора)
        # include_tables=False убирает таблицы (они ломают саммари)
        text = trafilatura.extract(
            downloaded, 
            include_comments=False, 
            include_tables=False,
            include_images=False,
            no_fallback=True
        )
        
        if not text:
            return ""
            
        # Возвращаем чистый текст
        return text

    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return ""