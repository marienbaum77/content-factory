# ==============================================================================
# КОМАНДЫ ДЛЯ ЛОКАЛЬНОЙ РАЗРАБОТКИ (с venv)
# ==============================================================================

# Общая команда для активации окружения и запуска сервиса
.PHONY: run-collector run-processor run-publisher

# Настройка PYTHONPATH и активация VENV
ACTIVATE_VENV := source venv/bin/activate; export PYTHONPATH=$$PYTHONPATH:$(PWD)/src;

run-collector:
	@echo "--- Запуск: Collector (Сборщик RSS) ---"
	@$(ACTIVATE_VENV) \
	python3 src/collector/main.py

run-processor:
	@echo "--- Запуск: Processor (Парсер и AI) ---"
	@$(ACTIVATE_VENV) \
	python3 src/processor/main.py

run-publisher:
	@echo "--- Запуск: Publisher (Отправка в Telegram) ---"
	@$(ACTIVATE_VENV) \
	python3 src/publisher/main.py

# ==============================================================================
# КОМАНДЫ ДЛЯ INFRASTRUCTURE (Docker)
# ==============================================================================

.PHONY: up down logs clean build

up:
	@echo "--- Запуск всего стека через Docker Compose ---"
	docker compose up -d

down:
	@echo "--- Остановка и удаление контейнеров ---"
	docker compose down

build:
	@echo "--- Сборка Docker-образа с no-cache ---"
	docker compose up -d --build --no-cache

logs:
	@echo "--- Мониторинг логов (Ctrl+C для выхода) ---"
	docker compose logs -f

clean:
	@echo "--- Удаление всех неиспользуемых образов и кэша ---"
	docker image prune -a -f
	docker builder prune -a -f
	@echo "--- Удаление таблиц в БД ---"
	# В реальной жизни это делается через миграции, а не вручную