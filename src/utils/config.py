"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_USERNAME: str = "lil_ken_ceo_bot"
    TELEGRAM_ADMIN_ID: Optional[int] = None
    
    # AI APIs
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: Optional[str] = None
    
    # Database
    REDIS_URL: str = "redis://localhost:6379"
    POSTGRES_URL: str = "postgresql://postgres:password@localhost:5432/lil_agents"
    
    # ChromaDB
    CHROMADB_HOST: str = "localhost"
    CHROMADB_PORT: int = 8000
    
    # n8n Integration
    N8N_WEBHOOK_URL: Optional[str] = None
    N8N_API_KEY: Optional[str] = None
    
    # Agent Configuration
    AGENT_NAME: str = "lil_ken_ceo"
    AGENT_LANGUAGE: str = "ru"
    LOG_LEVEL: str = "INFO"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    KNOWLEDGE_BASE_DIR: Path = DATA_DIR / "knowledge_base" / AGENT_NAME
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this"
    API_RATE_LIMIT: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Создаем глобальный экземпляр настроек
settings = Settings()

# Создаем необходимые директории
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)