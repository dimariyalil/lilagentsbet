"""
Управление памятью агента
"""
import json
import redis.asyncio as redis
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from utils.config import settings
from utils.logger import setup_logger

logger = setup_logger("memory")


class MemoryManager:
    """Менеджер памяти для агентов"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.redis = None
        self._connect()
    
    def _connect(self):
        """Подключение к Redis"""
        self.redis = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )
    
    async def add_message(
        self, 
        user_id: int, 
        user_message: str, 
        assistant_message: str
    ):
        """Добавление сообщения в историю"""
        key = f"{self.agent_name}:chat:{user_id}"
        
        message_data = {
            "user": user_message,
            "assistant": assistant_message,
            "timestamp": datetime.now().isoformat()
        }
        
        # Добавляем в список
        await self.redis.rpush(key, json.dumps(message_data))
        
        # Храним только последние 50 сообщений
        await self.redis.ltrim(key, -50, -1)
        
        # Устанавливаем TTL на 7 дней
        await self.redis.expire(key, timedelta(days=7))
    
    async def get_context(self, user_id: int) -> Dict[str, Any]:
        """Получение контекста диалога"""
        key = f"{self.agent_name}:chat:{user_id}"
        
        # Получаем последние 10 сообщений
        messages = await self.redis.lrange(key, -10, -1)
        
        history = []
        for msg in messages:
            history.append(json.loads(msg))
        
        return {
            "user_id": user_id,
            "history": history,
            "message_count": len(history)
        }
    
    async def clear_context(self, user_id: int):
        """Очистка контекста пользователя"""
        key = f"{self.agent_name}:chat:{user_id}"
        await self.redis.delete(key)
    
    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Получение статистики пользователя"""
        key = f"{self.agent_name}:stats:{user_id}"
        
        stats = await self.redis.hgetall(key)
        if not stats:
            stats = {
                "total_messages": 0,
                "first_interaction": None,
                "last_interaction": None
            }
        
        return stats
    
    async def update_user_stats(self, user_id: int):
        """Обновление статистики пользователя"""
        key = f"{self.agent_name}:stats:{user_id}"
        
        await self.redis.hincrby(key, "total_messages", 1)
        await self.redis.hset(key, "last_interaction", datetime.now().isoformat())
        
        # Устанавливаем first_interaction если это первое сообщение
        if not await self.redis.hexists(key, "first_interaction"):
            await self.redis.hset(
                key, 
                "first_interaction", 
                datetime.now().isoformat()
            )