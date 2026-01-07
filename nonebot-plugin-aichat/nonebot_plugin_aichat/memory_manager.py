# memory_manager.py
import json
import re
from pathlib import Path
from typing import Dict, Optional
from .config import cfg

class MemoryManager:
    def __init__(self):
        self.file_path = Path(cfg.memory_file)
        self.memory: Dict[str, dict] = {}
        self._initialize_memory()

    def _initialize_memory(self):
        if not self.file_path.exists():
            self.save_memory()
        self.load_memory()

    def load_memory(self):
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
        except Exception:
            self.memory = {}

    def save_memory(self):
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def search_memory(self, text: str) -> Optional[str]:
        if not text:
            return None
            
        found = []
        for keyword, data in self.memory.items():
            if re.search(re.escape(keyword), text, flags=re.IGNORECASE):
                found.append((data.get('weight', 1.0), data['content']))
        
        if not found:
            return None

        found.sort(reverse=True, key=lambda x: x[0])
        
        return "\n".join([f"[背景信息] {content}" for _, content in found[:3]])

    def add_memory(self, keyword: str, content: str, weight: float = 1.0):
        self.memory[keyword] = {
            "content": content,
            "weight": max(0.1, min(1.0, weight))
        }
        self.save_memory()

memory_manager = MemoryManager()