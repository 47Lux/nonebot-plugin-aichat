# web_admin.py
import json
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from nonebot import get_app, logger

from .config import cfg
from .memory_manager import memory_manager

app: FastAPI = get_app()
BASE_DIR = Path(__file__).parent.resolve()
STATIC_DIR = (BASE_DIR / "static").resolve()

if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/aichat/static", StaticFiles(directory=str(STATIC_DIR)), name="aichat_static")

def load_json_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"[AIChat] 读取 {file_path} 失败: {e}")
    return {}

def save_json_file(file_path, data):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logger.error(f"[AIChat] 写入 {file_path} 失败: {e}")
        return False

@app.get("/api/aichat/all_data")
async def get_all_data():
    exclude = ["config_json_path", "characters_file", "groups_file", "memory_file"]
    config_dict = {k: v for k, v in cfg.__dict__.items() if k not in exclude}
    
    return {
        "characters": load_json_file(cfg.characters_file),
        "groups": load_json_file(cfg.groups_file),
        "memory": memory_manager.memory,
        "config": config_dict
    }

@app.post("/api/aichat/save")
async def save_all_data(payload: dict):
    try:
        if "config" in payload:
            new_cfg = payload["config"]
            for k, v in new_cfg.items():
                if hasattr(cfg, k):
                    setattr(cfg, k, v)
            cfg.save()

        if "characters" in payload:
            save_json_file(cfg.characters_file, payload["characters"])
        
        if "groups" in payload:
            save_json_file(cfg.groups_file, payload["groups"])
            
        if "memory" in payload:
            memory_manager.memory = payload["memory"]
            memory_manager.save_memory()
            
        return {"status": "success"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/aichat/admin", response_class=HTMLResponse)
async def admin_page():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding='utf-8')
    return HTMLResponse(content="<h1>static/index.html 丢失</h1>", status_code=404)