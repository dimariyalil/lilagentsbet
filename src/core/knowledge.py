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
        self.client = None
        self.collection = None
        self.embedding_function = None
        self.memory_storage = []  # Fallback хранение в памяти
        
        try:
            self.client = chromadb.HttpClient(
                host=settings.CHROMADB_HOST,
                port=settings.CHROMADB_PORT
            )
            
            # Используем OpenAI embeddings
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            
            # Создаем или получаем коллекцию
            self.collection = self.client.get_or_create_collection(
                name=f"{agent_name}_knowledge",
                embedding_function=self.embedding_function
            )
            print(f"✅ ChromaDB подключен для агента {agent_name}")
        except Exception as e:
            print(f"⚠️ ChromaDB недоступен, используем память: {e}")
            self.client = None
    
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
            "timestamp": str(datetime.now()),
            "doc_id": doc_id
        })
        
        if self.client and self.collection:
            try:
                # Добавляем в ChromaDB
                self.collection.add(
                    documents=[content],
                    metadatas=[metadata],
                    ids=[doc_id]
                )
                logger.info(f"Document {doc_id} added to ChromaDB")
            except Exception as e:
                logger.error(f"Failed to add document to ChromaDB: {e}")
                # Fallback к хранению в памяти
                self.memory_storage.append({
                    "id": doc_id,
                    "content": content,
                    "metadata": metadata
                })
        else:
            # Используем хранение в памяти
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
        """Поиск по базе знаний"""
        if self.client and self.collection:
            try:
                # Поиск в ChromaDB
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
                return results
            except Exception as e:
                logger.error(f"Failed to search in ChromaDB: {e}")
        
        # Fallback поиск в памяти (простой текстовый поиск)
        matching_docs = []
        query_lower = query.lower()
        
        for doc in self.memory_storage:
            if query_lower in doc["content"].lower():
                matching_docs.append(doc)
        
        # Ограничиваем количество результатов
        matching_docs = matching_docs[:n_results]
        
        # Форматируем результат в стиле ChromaDB
        if matching_docs:
            return {
                "documents": [[doc["content"] for doc in matching_docs]],
                "metadatas": [[doc["metadata"] for doc in matching_docs]],
                "ids": [[doc["id"] for doc in matching_docs]]
            }
        
        return {"documents": [[]]}
    
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