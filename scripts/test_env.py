#!/usr/bin/env python3
"""
Скрипт для проверки наличия всех необходимых переменных окружения
"""
import os
import sys
from pathlib import Path

# Добавляем src в path для импорта настроек
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import settings


def check_environment_variables():
    """Проверяет наличие всех необходимых переменных окружения"""
    
    print("🔍 Проверка переменных окружения...\n")
    
    # Обязательные переменные
    required_vars = {
        "TELEGRAM_BOT_TOKEN": "Токен Telegram бота",
        "ANTHROPIC_API_KEY": "API ключ Claude/Anthropic",
    }
    
    # Опциональные переменные
    optional_vars = {
        "TELEGRAM_ADMIN_ID": "ID администратора бота",
        "OPENAI_API_KEY": "API ключ OpenAI",
        "REDIS_URL": "URL подключения к Redis",
        "POSTGRES_URL": "URL подключения к PostgreSQL",
        "CHROMADB_HOST": "Хост ChromaDB",
        "CHROMADB_PORT": "Порт ChromaDB",
        "N8N_WEBHOOK_URL": "URL webhook n8n",
        "N8N_API_KEY": "API ключ n8n",
        "SECRET_KEY": "Секретный ключ приложения",
    }
    
    all_good = True
    
    # Проверяем обязательные переменные
    print("📋 Обязательные переменные:")
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        if value and value.strip():
            print(f"  ✅ {var_name}: {description} - НАЙДЕНА")
        else:
            print(f"  ❌ {var_name}: {description} - НЕ НАЙДЕНА")
            all_good = False
    
    print()
    
    # Проверяем опциональные переменные
    print("📝 Опциональные переменные:")
    for var_name, description in optional_vars.items():
        value = os.getenv(var_name)
        if value and value.strip():
            print(f"  ✅ {var_name}: {description} - НАЙДЕНА")
        else:
            print(f"  ⚠️  {var_name}: {description} - НЕ НАЙДЕНА (опционально)")
    
    print()
    
    # Проверяем настройки из config
    print("⚙️  Текущие настройки:")
    print(f"  🤖 Bot Username: @{settings.TELEGRAM_BOT_USERNAME}")
    print(f"  🎯 Agent Name: {settings.AGENT_NAME}")
    print(f"  🌍 Language: {settings.AGENT_LANGUAGE}")
    print(f"  📝 Log Level: {settings.LOG_LEVEL}")
    
    # Проверяем доступность ключевых настроек
    if not settings.TELEGRAM_BOT_TOKEN:
        print("  ❌ TELEGRAM_BOT_TOKEN не настроен в settings")
        all_good = False
    
    if not settings.ANTHROPIC_API_KEY:
        print("  ❌ ANTHROPIC_API_KEY не настроен в settings")
        all_good = False
    
    print()
    
    # Итоговое сообщение
    if all_good:
        print("✅ Все обязательные переменные окружения настроены!")
        print("🚀 Бот готов к запуску")
        return True
    else:
        print("❌ Некоторые обязательные переменные не найдены!")
        print("🔧 Настройте их перед запуском бота")
        return False


def main():
    """Главная функция"""
    print("=" * 60)
    print("🔧 Проверка конфигурации lil_ken_ceo бота")
    print("=" * 60)
    print()
    
    success = check_environment_variables()
    
    print()
    print("=" * 60)
    
    if success:
        print("✅ Конфигурация корректна!")
        sys.exit(0)
    else:
        print("❌ Необходимо исправить конфигурацию!")
        sys.exit(1)


if __name__ == "__main__":
    main()