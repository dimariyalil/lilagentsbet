#!/bin/bash

# Активация виртуального окружения
source venv/bin/activate

# Экспорт переменных окружения
export $(cat .env | grep -v '^#' | xargs)

# Запуск с автоперезагрузкой
watchmedo auto-restart \
    --directory=./src \
    --pattern="*.py" \
    --recursive \
    -- python src/main.py