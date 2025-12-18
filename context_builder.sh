#!/bin/bash
# Скрипт для сборки контекста проекта для AI-анализа

OUTPUT_FILE="ai_context.txt"

# 1. Очищаем старый файл
> "$OUTPUT_FILE"

# 2. Список файлов в корне (requirements.txt, docker-compose.yml, .env)
ROOT_FILES=("requirements.txt" "docker-compose.yml" ".env")

echo "========================================
ROOT FILES
========================================" >> "$OUTPUT_FILE"

for file in "${ROOT_FILES[@]}"; do
    if [ -f "$file" ]; then
        printf "\n\n========================================\nFILE: %s\n========================================\n" "$file" >> "$OUTPUT_FILE"
        cat "$file" >> "$OUTPUT_FILE"
    else
        printf "\n\n========================================\nFILE: %s (Not Found)\n========================================\n" "$file" >> "$OUTPUT_FILE"
    fi
done

# 3. Рекурсивное копирование папки src (игнорируем кэш и окружение)
echo "\n\n========================================
SRC DIRECTORY (Application Code)
========================================" >> "$OUTPUT_FILE"

find src -type f \
  -not -path '*/.*' \
  -not -path '*/venv/*' \
  -not -path '*/__pycache__/*' \
  -not -name 'poetry.lock' \
  -not -name '*.pyc' \
  -exec printf "\n\n========================================\nFILE: {}\n========================================\n" \; \
  -exec cat {} \; >> "$OUTPUT_FILE"

echo "Контекст сохранен в файл: $OUTPUT_FILE"
