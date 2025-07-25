#!/usr/bin/env python3
"""
Загрузка базы знаний в ChromaDB
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.knowledge import KnowledgeBase
from utils.config import settings
from utils.logger import setup_logger

logger = setup_logger("knowledge_loader")


async def load_knowledge_base():
    """Загрузка документов в базу знаний"""
    kb = KnowledgeBase("lil_ken_ceo")
    await kb.initialize()
    
    knowledge_dir = settings.KNOWLEDGE_BASE_DIR
    
    # Загружаем все текстовые файлы
    for file_path in knowledge_dir.rglob("*.txt"):
        logger.info(f"Loading {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        metadata = {
            "source": str(file_path.relative_to(knowledge_dir)),
            "category": file_path.parent.name
        }
        
        await kb.add_document(content, metadata)
    
    # Загружаем markdown файлы
    for file_path in knowledge_dir.rglob("*.md"):
        logger.info(f"Loading {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        metadata = {
            "source": str(file_path.relative_to(knowledge_dir)),
            "category": file_path.parent.name,
            "format": "markdown"
        }
        
        await kb.add_document(content, metadata)
    
    doc_count = await kb.get_doc_count()
    logger.info(f"Loaded {doc_count} documents into knowledge base")


if __name__ == "__main__":
    asyncio.run(load_knowledge_base())