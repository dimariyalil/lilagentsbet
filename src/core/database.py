"""
Работа с PostgreSQL
"""
import asyncpg
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from utils.config import settings
from utils.logger import setup_logger

logger = setup_logger("database")


class Database:
    """Менеджер базы данных"""
    
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        """Создание пула соединений"""
        self.pool = await asyncpg.create_pool(
            settings.POSTGRES_URL,
            min_size=5,
            max_size=20
        )
        
        # Создаем таблицы если их нет
        await self._create_tables()
    
    async def _create_tables(self):
        """Создание необходимых таблиц"""
        async with self.pool.acquire() as conn:
            # Таблица пользователей
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    username VARCHAR(255),
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Таблица сообщений
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    agent_name VARCHAR(50),
                    user_message TEXT,
                    assistant_message TEXT,
                    tokens_used INTEGER,
                    response_time FLOAT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Таблица отчетов
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id SERIAL PRIMARY KEY,
                    agent_name VARCHAR(50),
                    report_type VARCHAR(50),
                    content TEXT,
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Индексы
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_user_agent 
                ON messages(user_id, agent_name)
            """)
            
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_reports_agent_type 
                ON reports(agent_name, report_type)
            """)
    
    async def get_or_create_user(
        self, 
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> int:
        """Получение или создание пользователя"""
        async with self.pool.acquire() as conn:
            # Пробуем найти пользователя
            user = await conn.fetchrow(
                "SELECT id FROM users WHERE telegram_id = $1",
                telegram_id
            )
            
            if user:
                # Обновляем информацию
                await conn.execute("""
                    UPDATE users 
                    SET username = $2, 
                        first_name = $3, 
                        last_name = $4,
                        updated_at = NOW()
                    WHERE telegram_id = $1
                """, telegram_id, username, first_name, last_name)
                return user['id']
            else:
                # Создаем нового пользователя
                user_id = await conn.fetchval("""
                    INSERT INTO users (telegram_id, username, first_name, last_name)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id
                """, telegram_id, username, first_name, last_name)
                return user_id
    
    async def save_message(
        self,
        user_id: int,
        agent_name: str,
        user_message: str,
        assistant_message: str,
        tokens_used: int = 0,
        response_time: float = 0
    ):
        """Сохранение сообщения"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO messages 
                (user_id, agent_name, user_message, assistant_message, 
                 tokens_used, response_time)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, user_id, agent_name, user_message, assistant_message, 
                tokens_used, response_time)
    
    async def save_report(
        self,
        agent_name: str,
        report_type: str,
        content: str,
        metadata: Dict[str, Any]
    ):
        """Сохранение отчета"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO reports (agent_name, report_type, content, metadata)
                VALUES ($1, $2, $3, $4)
            """, agent_name, report_type, content, json.dumps(metadata))
    
    async def get_user_stats(self, telegram_id: int) -> Dict[str, Any]:
        """Получение статистики пользователя"""
        async with self.pool.acquire() as conn:
            stats = await conn.fetchrow("""
                SELECT 
                    COUNT(*) as total_messages,
                    MIN(created_at) as first_message,
                    MAX(created_at) as last_message,
                    AVG(response_time) as avg_response_time
                FROM messages m
                JOIN users u ON m.user_id = u.id
                WHERE u.telegram_id = $1
            """, telegram_id)
            
            return dict(stats) if stats else {}
    
    async def close(self):
        """Закрытие пула соединений"""
        if self.pool:
            await self.pool.close()