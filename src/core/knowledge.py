"""
База знаний на ChromaDB
"""
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional
import hashlib
import json
from datetime import datetime

from utils.config import settings
from utils.logger import setup_logger

logger = setup_logger("knowledge")


class KnowledgeBase:
    """База знаний агента"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.client = chromadb.HttpClient(
            host=settings.CHROMADB_HOST,
            port=settings.CHROMADB_PORT
        )
        
        # Используем OpenAI embeddings
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = None
    
    async def initialize(self):
        """Инициализация коллекции"""
        try:
            self.collection = self.client.get_or_create_collection(
                name=f"{self.agent_name}_knowledge",
                embedding_function=self.embedding_function
            )
            logger.info(f"Knowledge base initialized for {self.agent_name}")
        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {e}")
            raise
    
    async def add_document(
        self, 
        content: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Добавление документа в базу знаний"""
        # Генерируем ID документа
        doc_id = hashlib.md5(content.encode()).hexdigest()
        
        # Добавляем метаданные
        if metadata is None:
            metadata = {}
        
        metadata.update({
            "agent": self.agent_name,
            "timestamp": datetime.now().isoformat()
        })
        
        # Добавляем в коллекцию
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        logger.info(f"Added document {doc_id} to knowledge base")
        return doc_id
    
    async def search(
        self, 
        query: str, 
        n_results: int = 5
    ) -> Dict[str, Any]:
        """Поиск по базе знаний"""
        if not self.collection:
            return {"documents": []}
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Форматируем результаты
            documents = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0
                    })
            
            return {
                "query": query,
                "documents": documents,
                "count": len(documents)
            }
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {"documents": []}
    
    async def get_doc_count(self) -> int:
        """Получение количества документов"""
        if not self.collection:
            return 0
        
        return self.collection.count()
    
    async def delete_document(self, doc_id: str):
        """Удаление документа"""
        self.collection.delete(ids=[doc_id])
        logger.info(f"Deleted document {doc_id}")
    
    async def update_document(
        self, 
        doc_id: str, 
        content: str, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Обновление документа"""
        self.collection.update(
            ids=[doc_id],
            documents=[content],
            metadatas=[metadata] if metadata else None
        )
        logger.info(f"Updated document {doc_id}")