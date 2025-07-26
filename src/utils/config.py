"""
Конфигурация приложения
"""
import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional
from pathlib import Path


def get_env_var(key: str, default: Optional[str] = None) -> str:
    """
    Получает переменную окружения с fallback на .env файл
    Сначала проверяет переменные окружения (для GitHub Actions),
    затем загружает из .env файла (для локальной разработки)
    """
    value = os.getenv(key)
    if value is not None:
        return value
    
    # Если переменная не найдена в окружении, пытаемся загрузить из .env
    env_file_path = Path(__file__).parent.parent.parent / ".env"
    if env_file_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file_path)
            return os.getenv(key, default)
        except ImportError:
            # dotenv не установлен, возвращаем default
            pass
    
    return default


def get_env_int(key: str, default: Optional[int] = None) -> Optional[int]:
    """Безопасно получает целочисленную переменную окружения"""
    value = get_env_var(key, "")
    if not value or not value.strip():
        return default
    try:
        return int(value.strip())
    except ValueError:
        return default


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = get_env_var("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_BOT_USERNAME: str = "LilagentsbetBot"  # Реальное имя бота
    TELEGRAM_ADMIN_ID: Optional[str] = get_env_var("TELEGRAM_ADMIN_ID", "")
    
    @field_validator('TELEGRAM_ADMIN_ID')
    @classmethod
    def validate_admin_id(cls, v):
        if not v or not v.strip():
            return None
        try:
            return int(v.strip())
        except ValueError:
            return None
    
    # AI APIs
    ANTHROPIC_API_KEY: str = get_env_var("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: Optional[str] = get_env_var("OPENAI_API_KEY")
    
    # Database
    REDIS_URL: str = get_env_var("REDIS_URL", "redis://localhost:6379")
    POSTGRES_URL: str = get_env_var("POSTGRES_URL", "postgresql://postgres:password@localhost:5432/lil_agents")
    
    # ChromaDB
    CHROMADB_HOST: str = get_env_var("CHROMADB_HOST", "localhost")
    CHROMADB_PORT: int = int(get_env_var("CHROMADB_PORT", "8000"))
    
    # n8n Integration
    N8N_WEBHOOK_URL: Optional[str] = get_env_var("N8N_WEBHOOK_URL")
    N8N_API_KEY: Optional[str] = get_env_var("N8N_API_KEY")
    
    # Agent Configuration
    AGENT_NAME: str = get_env_var("AGENT_NAME", "lil_ken_ceo")
    AGENT_LANGUAGE: str = get_env_var("AGENT_LANGUAGE", "ru")
    LOG_LEVEL: str = get_env_var("LOG_LEVEL", "INFO")
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    KNOWLEDGE_BASE_DIR: Path = DATA_DIR / "knowledge_base" / AGENT_NAME
    
    # Security
    SECRET_KEY: str = get_env_var("SECRET_KEY", "your-secret-key-change-this")
    API_RATE_LIMIT: int = int(get_env_var("API_RATE_LIMIT", "100"))
    
    class Config:
        case_sensitive = True


# Создаем глобальный экземпляр настроек
settings = Settings()

# Создаем необходимые директории
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)