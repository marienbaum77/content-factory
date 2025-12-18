FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Объявляем переменную сборки. По умолчанию - официальный сервер.
ARG APT_MIRROR=deb.debian.org

# Используем эту переменную для подмены
# Если передадим mirror.yandex.ru - будет Яндекс. Если ничего - будет Debian.
RUN sed -i "s/deb.debian.org/${APT_MIRROR}/g" /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    sed -i "s/deb.debian.org/${APT_MIRROR}/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

COPY src/processor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Скачиваем ОБА пакета: punkt (старый стандарт) и punkt_tab (новый, обязателен для NLTK 3.9+)
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
COPY src/ /app/src/

CMD ["python", "src/processor/main.py"]