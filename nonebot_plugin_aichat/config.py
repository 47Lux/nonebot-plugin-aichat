import os
import json
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, Any

# 1. 定义符合 NoneBot 标准的配置类
class PluginConfig(BaseModel):
    command_prefix: str = "#"
    reply_probability: float = 0.2
    system_prompt: str = "你是路芸笙"
    api_url: str = ""
    api_key: str = ""
    max_chat_history: int = 11
    model_settings: Dict[str, Any] = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7
    }
    speaker_memory_template: str = "关于 {nickname} 的记忆：{memory_content}"
    reply_prefix_template: str = "回答 {nickname} 在 {groupname} 说的："

    # 数据文件路径（这些不作为配置项，所以不写在上面）
    @property
    def base_path(self) -> Path:
        p = Path(__file__).parent / "data"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def config_json_path(self) -> Path: return self.base_path / "config.json"
    @property
    def characters_file(self) -> str: return str(self.base_path / "characters.json")
    @property
    def groups_file(self) -> str: return str(self.base_path / "groups.json")
    @property
    def memory_file(self) -> str: return str(self.base_path / "memory.json")

    def load(self):
        if self.config_json_path.exists():
            try:
                with open(self.config_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 将读取到的数据更新到当前模型
                    for key, value in data.items():
                        if hasattr(self, key):
                            setattr(self, key, value)
            except Exception:
                pass

    def save(self):
        # 仅保存配置项数据，排除掉路径方法
        data = self.model_dump(exclude={
            "base_path", "config_json_path", "characters_file", 
            "groups_file", "memory_file"
        })
        with open(self.config_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# 2. 实例化并执行初次加载
cfg = PluginConfig()
cfg.load()
