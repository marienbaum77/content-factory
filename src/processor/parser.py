import httpx
from bs4 import BeautifulSoup
from config import settings

async def fetch_text_from_url(url: str) -> str:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            headers = {"User-Agent": settings.user_agent}
            response = await client.get(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            
            # Парсим HTML
            soup = BeautifulSoup(response.text, "lxml")
            
            # Удаляем мусор (скрипты, стили)
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.extract()
            
            # Достаем текст. Ограничим 3000 символов, чтобы не забивать консоль
            text = soup.get_text(separator="\n", strip=True)
            return text[:3000] 
            
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""