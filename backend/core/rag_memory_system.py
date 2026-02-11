import os
import uuid
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import chromadb
from chromadb.utils import embedding_functions

logger = logging.getLogger("omni_genesis.memory")

class RAGMemorySystem:
    """
    RAG Memory System powered by ChromaDB.
    Provides persistent vector storage, semantic retrieval, and interaction logging.
    """
    def __init__(self, config: Dict[str, Any] = None):
        config = config or {}
        dataset_path = config.get("memory_path", "learning_set")
        
        self.dataset_path = Path(dataset_path)
        self.persist_dir = "./chroma_db"
        
        # Initialize ChromaDB (Persistent)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        # Use default embedding function (all-MiniLM-L6-v2)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(
            name="namo_knowledge",
            embedding_function=self.embedding_fn
        )
        
        # Auto-ingest if empty
        if self.collection.count() == 0:
            self.ingest_data()

    def ingest_data(self):
        """Scans dataset_path and ingests text files into ChromaDB."""
        if not self.dataset_path.exists():
            logger.warning("memory_path_missing", extra={"path": str(self.dataset_path)})
            return

        logger.info("memory_scan_start", extra={"path": str(self.dataset_path)})
        files = list(self.dataset_path.glob("**/*.txt")) + list(self.dataset_path.glob("**/*.md"))
        
        documents = []
        metadatas = []
        ids = []

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    # Simple chunking (500 chars)
                    chunks = [content[i:i+500] for i in range(0, len(content), 500)]
                    
                    for idx, chunk in enumerate(chunks):
                        if len(chunk.strip()) < 10: continue
                        
                        documents.append(chunk)
                        metadatas.append({"source": str(file_path.name), "type": "knowledge_base"})
                        ids.append(f"{file_path.name}_{idx}_{str(uuid.uuid4())[:8]}")
            except Exception as e:
                logger.error("memory_file_read_error", extra={"file": str(file_path), "error": str(e)})

        if documents:
            logger.info("memory_upsert_start", extra={"chunk_count": len(documents)})
            # Batch upsert
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                end = min(i + batch_size, len(documents))
                self.collection.upsert(
                    documents=documents[i:end],
                    metadatas=metadatas[i:end],
                    ids=ids[i:end]
                )
            logger.info("memory_ingestion_complete")

    def retrieve(self, query: str, top_k: int = 3) -> str:
        """Retrieves relevant context for a given query."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            if not results['documents'] or not results['documents'][0]:
                return ""
                
            # Combine retrieved documents
            context = "\n".join(results['documents'][0])
            return context
        except Exception as e:
            logger.error("memory_retrieval_error", extra={"error": str(e)})
            return ""

    def save_interaction(self, user_input: str, response: str):
        """Saves the interaction to short-term memory (Vector DB)."""
        try:
            interaction_text = f"User: {user_input}\nNamo: {response}"
            self.collection.add(
                documents=[interaction_text],
                metadatas=[{"type": "conversation_history", "timestamp": str(os.times())}],
                ids=[f"chat_{str(uuid.uuid4())}"]
            )
        except Exception as e:
            logger.error("memory_save_error", extra={"error": str(e)})
