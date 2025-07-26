"""
Главный класс CEO агента
"""
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any

from anthropic import AsyncAnthropic

from .prompts import CEO_PROMPTS
from .commands import CEOCommands
from core.memory import MemoryManager
from core.knowledge import KnowledgeBase
from utils.config import settings
from utils.logger import setup_logger

logger = setup_logger("lil_ken_ceo")


class LilKenCEO:
    """CEO Agent - Стратегический директор"""
    
    def __init__(self):
        self.name = "lil_ken_ceo"
        self.anthropic = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.memory = MemoryManager(self.name)
        self.knowledge = KnowledgeBase(self.name)
        self.commands = CEOCommands(self)
        self.initialized = False
    
    async def initialize(self):
        """Инициализация агента"""
        if self.initialized:
            return
        
        logger.info(f"Initializing {self.name}...")
        
        # Инициализируем базу знаний
        await self.knowledge.initialize()
        
        # Загружаем начальные данные
        await self._load_initial_knowledge()
        
        self.initialized = True
        logger.info(f"{self.name} initialized successfully")
    
    async def _load_initial_knowledge(self):
        """Загрузка начальной базы знаний"""
        # Здесь будет загрузка документов из knowledge_base
        pass
    
    async def process_message(self, message: str, user_id: int) -> str:
        """Обработка сообщения от пользователя"""
        try:
            # Получаем контекст из памяти
            context = await self.memory.get_context(user_id)
            
            # Ищем релевантную информацию в базе знаний
            knowledge_context = await self.knowledge.search(message)
            
            # Формируем промпт
            prompt = self._build_prompt(message, context, knowledge_context)
            
            # Получаем ответ от Claude
            response = await self._get_ai_response(prompt)
            
            # Сохраняем в память
            await self.memory.add_message(user_id, message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return "Произошла ошибка при обработке запроса. Попробуйте позже."
    
    def _build_prompt(
        self, 
        message: str, 
        context: Dict[str, Any], 
        knowledge: Dict[str, Any]
    ) -> str:
        """Построение промпта для AI"""
        system_prompt = CEO_PROMPTS["system"]
        
        prompt_parts = [
            system_prompt,
            f"\nТекущая дата: {datetime.now().strftime('%Y-%m-%d')}",
        ]
        
        if knowledge.get("documents"):
            prompt_parts.append("\nРелевантная информация из базы знаний:")
            for doc in knowledge["documents"][:3]:
                prompt_parts.append(f"- {doc['content'][:500]}...")
        
        if context.get("history"):
            prompt_parts.append("\nПоследние сообщения:")
            for msg in context["history"][-5:]:
                prompt_parts.append(f"User: {msg['user']}")
                prompt_parts.append(f"Assistant: {msg['assistant']}")
        
        prompt_parts.append(f"\nТекущий запрос пользователя: {message}")
        
        return "\n".join(prompt_parts)
    
    async def _get_ai_response(self, prompt: str) -> str:
        """Получение ответа от Claude"""
        try:
            response = await self.anthropic.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            raise
    
    # Методы для команд
    async def generate_year_strategy(self) -> str:
        """Генерация годовой стратегии"""
        return await self.commands.year_strategy()
    
    async def analyze_market(self, country: str) -> str:
        """Анализ рынка страны"""
        return await self.commands.market_analysis(country)
    
    async def competitor_analysis(self) -> str:
        """Анализ конкурентов"""
        return await self.commands.competitor_watch()
    
    async def swot_analysis(self) -> str:
        """SWOT анализ"""
        return await self.commands.swot_analysis()
    
    async def risk_assessment(self) -> str:
        """Оценка рисков"""
        return await self.commands.risk_assessment()
    
    async def daily_report(self) -> str:
        """Ежедневный отчет"""
        return await self.commands.daily_report()
    
    async def weekly_report(self) -> str:
        """Недельный отчет"""  
        return await self.commands.weekly_report()
    
    async def get_status(self) -> str:
        """Получение статуса системы"""
        return await self.commands.status()