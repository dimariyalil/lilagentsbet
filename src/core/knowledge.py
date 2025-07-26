"""
Упрощенная база знаний (только в памяти)
"""
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Упрощенная база знаний агента (только в памяти)"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.memory_storage: List[Dict[str, Any]] = []  # Хранение в памяти
        logger.info(f"✅ In-memory knowledge base initialized for {agent_name}")
    
    async def initialize(self):
        """Инициализация базы знаний"""
        logger.info(f"Knowledge base for {self.agent_name} ready")
        return True
    
    async def add_document(
        self,
        content: str,
        doc_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Добавление документа в базу знаний"""
        if metadata is None:
            metadata = {}
        
        # Добавляем системные метаданные
        metadata.update({
            "agent": self.agent_name,
            "timestamp": str(datetime.now()),
            "doc_id": doc_id
        })
        
        # Сохраняем в памяти
        self.memory_storage.append({
            "id": doc_id,
            "content": content,
            "metadata": metadata
        })
        
        logger.info(f"Document {doc_id} added to memory storage")
        return doc_id
    
    async def search(
        self,
        query: str,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """Простой поиск в памяти"""
        matching_docs = []
        query_lower = query.lower()
        
        for doc in self.memory_storage:
            if query_lower in doc["content"].lower():
                matching_docs.append(doc)
        
        # Ограничиваем количество результатов
        matching_docs = matching_docs[:n_results]
        
        # Форматируем результат
        if matching_docs:
            return {
                "documents": [[doc["content"] for doc in matching_docs]],
                "metadatas": [[doc["metadata"] for doc in matching_docs]],
                "ids": [[doc["id"] for doc in matching_docs]]
            }
        
        return {"documents": [[]]}
    
    async def get_doc_count(self) -> int:
        """Получение количества документов"""
        return len(self.memory_storage)