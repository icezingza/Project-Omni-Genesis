import glob
import json
import os
import random
import time
from pathlib import Path
from typing import List, Optional

import faiss
import numpy as np
# from openai import OpenAI # Uncomment in production

class RAGMemorySystem:
    """
    ระบบความจำนิรันดร์: อ่านไฟล์นิยายจริงๆ ของคุณจาก learning_set
    """
    def __init__(self, dataset_path: str | Path = "learning_set"):
        self.dataset_path = Path(dataset_path)
        self.vector_db = Path("vector_db")
        self.meta_path = self.vector_db / "meta.json"
        self.index_path = self.vector_db / "knowledge.index"
        self._faiss_index = None
        self._faiss_meta: list[dict] = []
        # self.client = OpenAI() # Initialize in production
        self.memories = []
        self.is_loaded = False

    def ingest_data(self):
        """อ่านไฟล์ .txt และ .htm ทั้งหมดในโฟลเดอร์"""
        if not self.dataset_path.exists():
            print(f"[Warning]: Path {self.dataset_path} does not exist.")
            self.memories = ["Placeholder memory 1", "Placeholder memory 2"]
            return

        print(f"[Memory System]: กำลังแสกนพื้นที่ {self.dataset_path} ...")
        
        txt_files = glob.glob(str(self.dataset_path / "**" / "*.txt"), recursive=True)
        htm_files = glob.glob(str(self.dataset_path / "**" / "*.htm"), recursive=True)
        all_files = txt_files + htm_files

        if not all_files:
            print("[Warning]: ไม่พบไฟล์นิยาย!")
            self.memories = ["Standard personality data loaded."]
            return

        for file_path in all_files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    chunks = [content[i:i+300] for i in range(0, len(content), 300)]
                    self.memories.extend(chunks)
            except Exception as e:
                print(f"อ่านไฟล์ {file_path} ไม่ได้: {e}")

        self._load_vector_index()
        self.is_loaded = True

    def _load_vector_index(self):
        if self.meta_path.exists() and self.index_path.exists():
            try:
                self._faiss_meta = json.load(open(self.meta_path, encoding="utf-8"))
                self._faiss_index = faiss.read_index(str(self.index_path))
            except Exception as e:
                print(f"[Memory System]: Load error: {e}")

    def retrieve_context(self, user_input: str) -> str:
        if not self.is_loaded:
            self.ingest_data()
        
        # In real case, use vector search here. Fallback to random for now.
        if self.memories:
            return random.choice(self.memories)
        return ""
