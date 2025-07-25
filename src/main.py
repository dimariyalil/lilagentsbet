#!/usr/bin/env python3
"""
Главный файл запуска lil_ken_ceo агента
"""
import asyncio
import logging
import sys
from pathlib import Path

# Добавляем src в path
sys.path.insert(0, str(Path(__file__).parent))

from core.bot import CEOBot
from utils.config import settings
from utils.logger import setup_logger

# Настройка логирования
logger = setup_logger("main")


async def main():
    """Главная функция запуска"""
    logger.info(f"Starting {settings.AGENT_NAME} bot...")
    
    try:
        # Создаем и запускаем бота
        bot = CEOBot()
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass