import os, json

class PluginConfig:
    def __init__(self):
        self.command_prefix = "#"          # 命令触发前缀
        self.reply_probability = 0.2       # 自动回复概率
        self.system_prompt = "你是路芸笙"   # 角色设定
        self.api_url = ""                  # API 地址
        self.api_key = ""                  # API 密钥
        self.max_chat_history = 11         # 上下文轮数
        self.model_settings = {            # 模型生成参数
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        }
        self.speaker_memory_template = "关于 {nickname} 的记忆：{memory_content}"
        self.reply_prefix_template = "回答 {nickname} 在 {groupname} 说的："


        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        os.makedirs(base_path, exist_ok=True)
        self.config_json_path = os.path.join(base_path, "config.json")
        self.characters_file = os.path.join(base_path, "characters.json")
        self.groups_file = os.path.join(base_path, "groups.json")
        self.memory_file = os.path.join(base_path, "memory.json")

 
        self.load()

    def load(self):
        if os.path.exists(self.config_json_path):
            try:
                with open(self.config_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.__dict__.update(data)
            except Exception: 
                pass

    def save(self):
        exclude = ["config_json_path", "characters_file", "groups_file", "memory_file"]
        data = {k: v for k, v in self.__dict__.items() if k not in exclude}
        with open(self.config_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

cfg = PluginConfig()