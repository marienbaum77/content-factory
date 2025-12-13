# 1. Используем конкретную стабильную версию (Debian 12 Bookworm), а не просто slim
FROM python:3.11-slim-bookworm

# 2. Переключаем зеркала Debian на Яндекс (для скорости в РФ)
# Мы меняем адрес в файле настроек apt прямо внутри образа перед обновлением
RUN sed -i 's/deb.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list.d/debian.sources

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# 3. Устанавливаем системные зависимости
# Теперь это пролетит мгновенно
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Библиотеки Python
COPY requirements.txt .
# Увеличиваем тайм-аут для pip на всякий случай
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# 5. NLTK
RUN python -m nltk.downloader punkt

# 6. Код
COPY src/ ./src/

# 7. Пользователь
RUN useradd -m appuser
USER appuser

CMD ["python", "src/collector/main.py"]