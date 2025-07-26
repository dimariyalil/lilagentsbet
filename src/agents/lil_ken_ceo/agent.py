"""
Упрощенный CEO агент
"""
import logging
from datetime import datetime
from typing import Optional

from anthropic import AsyncAnthropic
from utils.config import settings

logger = logging.getLogger(__name__)


class LilKenCEO:
    """Упрощенный CEO Agent"""
    
    def __init__(self):
        self.name = "lil_ken_ceo"
        self.anthropic = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.memory = {}  # Простая память в словаре
        self.initialized = False
    
    async def initialize(self):
        """Инициализация агента"""
        self.initialized = True
        logger.info(f"✅ {self.name} agent initialized")
        return True
    
    async def process_message(self, message: str, user_id: int) -> str:
        """Обработка сообщения пользователя"""
        try:
            # Простой запрос к Claude
            response = await self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"""Ты опытный CEO и бизнес-консультант. Отвечай профессионально и полезно.
                    
Вопрос: {message}

Дай краткий, но ценный совет как успешный руководитель."""
                }]
            )
            
            answer = response.content[0].text
            
            # Сохраняем в простую память
            if user_id not in self.memory:
                self.memory[user_id] = []
            self.memory[user_id].append({
                "message": message,
                "response": answer,
                "timestamp": datetime.now().isoformat()
            })
            
            return answer
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "Извините, произошла ошибка. Попробуйте еще раз."
    
    # Простые методы для команд
    async def generate_year_strategy(self) -> str:
        """Генерация годовой стратегии"""
        prompt = """Создай краткую годовую стратегию для стартапа:
- Ключевые цели на год
- Основные метрики
- План действий по кварталам
- Потенциальные риски"""
        
        try:
            response = await self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Ошибка: {e}"
    
    async def analyze_market(self, country: str) -> str:
        """Анализ рынка"""
        prompt = f"""Проведи краткий анализ рынка {country}:
- Размер рынка
- Ключевые игроки
- Возможности для входа
- Основные вызовы"""
        
        try:
            response = await self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Ошибка: {e}"
    
    async def competitor_analysis(self) -> str:
        """Анализ конкурентов"""
        prompt = """Создай шаблон для анализа конкурентов:
- Методы поиска конкурентов
- Ключевые метрики для сравнения
- Анализ слабых и сильных сторон
- Выводы и рекомендации"""
        
        try:
            response = await self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Ошибка: {e}"
    
    async def swot_analysis(self) -> str:
        """SWOT анализ"""
        prompt = """Создай шаблон SWOT анализа для стартапа:
- Strengths (Сильные стороны)
- Weaknesses (Слабые стороны)  
- Opportunities (Возможности)
- Threats (Угрозы)"""
        
        try:
            response = await self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Ошибка: {e}"
    
    async def risk_assessment(self) -> str:
        """Оценка рисков"""
        prompt = """Создай краткую оценку основных бизнес-рисков:
- Финансовые риски
- Операционные риски
- Рыночные риски
- Стратегические риски
- Методы снижения рисков"""
        
        try:
            response = await self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Ошибка: {e}"
    
    async def daily_report(self) -> str:
        """Ежедневный отчет"""
        return f"""📋 **Ежедневный отчет CEO**

📅 **Дата:** {datetime.now().strftime('%d.%m.%Y')}

🎯 **Приоритеты на сегодня:**
• Проверка ключевых метрик
• Встречи с командой  
• Работа над стратегическими задачами

📊 **Что отслеживать:**
• Выручку и расходы
• Активность пользователей
• Прогресс по целям

💡 **Рекомендации:**
• Сосредоточьтесь на 3 главных задачах
• Проведите 1:1 с ключевыми сотрудниками
• Обновите инвесторов о прогрессе"""
    
    async def weekly_report(self) -> str:
        """Недельный отчет"""
        return f"""📅 **Недельный отчет CEO**

🗓 **Неделя:** {datetime.now().strftime('%d.%m.%Y')}

🎯 **Достижения недели:**
• Выполненные цели
• Ключевые решения
• Прогресс команды

📈 **Метрики:**
• Рост пользователей
• Финансовые показатели
• Продуктивность команды

🔮 **Планы на следующую неделю:**
• Стратегические инициативы
• Важные встречи
• Критические задачи"""