"""
Настройка логирования
"""
import logging
import sys
from pathlib import Path
from pythonjsonlogger import jsonlogger
from datetime import datetime


def setup_logger(name: str) -> logging.Logger:
    """Настройка логгера"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Создаем директорию для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Форматтер для консоли
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # JSON форматтер для файлов
    json_formatter = jsonlogger.JsonFormatter()
    
    # Консольный handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Файловый handler
    file_handler = logging.FileHandler(
        log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)
    
    return logger