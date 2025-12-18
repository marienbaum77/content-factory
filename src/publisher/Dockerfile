FROM dockerhub.timeweb.cloud/library/python:3.11-slim

WORKDIR /app

# Отключаем создание .pyc файлов и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Копируем только зависимости паблишера
COPY src/publisher/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВЕСЬ код (потому что нам нужны common/storage модули)
COPY src/ /app/src/

# Запускаем
CMD ["python", "src/publisher/main.py"]