"""
Простая память в оперативной памяти
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class MemoryManager:
    """Простой менеджер памяти в оперативной памяти"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.memory: Dict[str, Any] = {}
        self.conversations: Dict[int, list] = {}
        logger.info(f"✅ Memory manager initialized for {agent_name}")
    
    async def initialize(self):
        """Инициализация памяти"""
        logger.info(f"Memory manager for {self.agent_name} ready")
        return True
    
    async def save_conversation(self, user_id: int, message: str, response: str):
        """Сохранение разговора"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "bot_response": response
        })
        
        # Ограничиваем историю последними 50 сообщениями
        if len(self.conversations[user_id]) > 50:
            self.conversations[user_id] = self.conversations[user_id][-50:]
    
    async def get_conversation_history(self, user_id: int, limit: int = 10) -> list:
        """Получение истории разговора"""
        if user_id not in self.conversations:
            return []
        return self.conversations[user_id][-limit:]
    
    async def set(self, key: str, value: Any):
        """Сохранение значения"""
        self.memory[key] = value
    
    async def get(self, key: str) -> Optional[Any]:
        """Получение значения"""
        return self.memory.get(key)
    
    async def delete(self, key: str):
        """Удаление значения"""
        if key in self.memory:
            del self.memory[key]
    
    async def clear_user_data(self, user_id: int):
        """Очистка данных пользователя"""
        if user_id in self.conversations:
            del self.conversations[user_id]