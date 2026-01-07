# __init__.py
import os
import json
import random
import re
import httpx
from nonebot import logger, on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from .config import cfg
from .memory_manager import memory_manager
from .web_admin import * 


chat_history = {}


def load_local_data(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"加载文件 {file_path} 失败: {e}")
        return {}

def remove_cq_code(message: str) -> str:
    """移除消息中的 CQ 码（如图片、表情等标签）"""
    return re.sub(r'\[CQ:[^\]]+\]', '', message)


async def call_language_model(bot: Bot, event: Event, message: str, nickname: str, groupname: str):
    user_id = event.get_user_id()
    group_id = getattr(event, 'group_id', 'private')
    chat_history_key = f"{group_id}_{user_id}"
    
    messages = chat_history.get(chat_history_key, [])
    if not messages:

        messages.append({"role": "system", "content": getattr(cfg, "system_prompt", "你是路芸笙")})


    mem_context = memory_manager.search_memory(message)
    if mem_context:
        messages.append({"role": "system", "content": mem_context})

    speaker_mem = memory_manager.search_memory(nickname)
    if speaker_mem:
        template = getattr(cfg, "speaker_memory_template", "关于 {nickname} 的记忆：{memory_content}")
        try:
            formatted_mem = template.format(nickname=nickname, memory_content=speaker_mem)
            messages.append({"role": "system", "content": formatted_mem})
        except:
            messages.append({"role": "system", "content": f"关于{nickname}的记忆：{speaker_mem}"})


    reply_prefix_raw = getattr(cfg, "reply_prefix_template", "回答 {nickname} 在 {groupname} 说的：")
    try:
        prefix = reply_prefix_raw.format(nickname=nickname, groupname=groupname)
    except:
        prefix = f"{nickname}说："
    
    messages.append({"role": "user", "content": f"{prefix} {message}"})


    model_params = getattr(cfg, "model_settings", {})
    payload = {**model_params, "messages": messages}
    headers = {
        "Authorization": f"Bearer {getattr(cfg, 'api_key', '')}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(cfg.api_url, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                res_json = response.json()
                reply = res_json["choices"][0]["message"]["content"].strip()
                messages.append({"role": "assistant", "content": reply})
                
             
                max_history = getattr(cfg, "max_chat_history", 11)
                if len(messages) > max_history:
                    messages = [messages[0]] + messages[-(max_history - 1):]
                
                chat_history[chat_history_key] = messages
                await bot.send(event, reply)
            else:
                logger.error(f"API 返回错误: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"AI 调用异常: {e}")


chat_matcher = on_message(priority=2, block=False)

@chat_matcher.handle()
async def handle_chat(bot: Bot, event: Event):

    if hasattr(cfg, "load"):
        cfg.load()

    raw_text = str(event.get_message())
    if any(tag in raw_text for tag in ["[CQ:image,", "[CQ:face,", "[CQ:record,"]):
        return

    msg_clean = remove_cq_code(raw_text).strip()
    if not msg_clean:
        return


    characters = load_local_data(cfg.characters_file)
    groups = load_local_data(cfg.groups_file)

    user_id = str(event.get_user_id())
    group_id = str(getattr(event, 'group_id', 'private'))

    nickname = characters.get(user_id, "陌生人")
    groupname = groups.get(group_id, "某个地方")


    cmd_prefix = getattr(cfg, "command_prefix", "#")
    

    if msg_clean.startswith(cmd_prefix):
        user_input = msg_clean[len(cmd_prefix):].strip()
        await call_language_model(bot, event, user_input, nickname, groupname)
    
    elif random.random() < getattr(cfg, "reply_probability", 0.0):
        await call_language_model(bot, event, msg_clean, nickname, groupname)