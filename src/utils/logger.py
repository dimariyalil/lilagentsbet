"""
Простая система логирования
"""
import logging
import sys
from pathlib import Path


def setup_logger(name: str = "bot") -> logging.Logger:
    """Настройка простого логгера"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Создаем обработчик для консоли
        handler = logging.StreamHandler(sys.stdout)
        
        # Простой формат
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger