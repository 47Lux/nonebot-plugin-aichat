# nonebot-plugin-aichat
支持Deepseek大模型官方API的角色扮演对话插件。/A NoneBot2 plugin for role-playing chat powered by official DeepSeek API, featuring dynamic personality and memory management.
nonebot-plugin-aichat
<p align="center"> <a href="https://v2.nonebot.dev/"><img src="https://img.shields.io/badge/nonebot-v2-red.svg" alt="nonebot"></a> <a href="https://pypi.org/project/nonebot-plugin-aichat/"><img src="https://img.shields.io/pypi/v/nonebot-plugin-aichat.svg" alt="pypi"></a> <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python"> <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="license"> </p>

一套支持 DeepSeek 官方 API 的角色扮演对话插件，内置 Web 可视化管理面板。

A role-play chat plugin supporting official DeepSeek API, featuring a built-in web management panel.





 功能特点 | Features
 角色扮演强化：支持自定义 System Prompt，打造专属人格。

 可视化管理：内置 Web 面板，无需手动修改 JSON 配置文件。

 身份/群组映射：支持 User ID → 昵称、Group ID → 群名的映射，让 AI 更懂对话环境。

 智能交互：支持前缀触发（如 #）及自定义概率的主动回复。

 记忆管理：支持关键词触发的长期记忆检索。

 安装 | Installation
使用 nb-cli 安装（推荐）：

```bash
nb plugin install nonebot-plugin-aichat
```
```bash
pip install nonebot-plugin-aichat
```




 管理面板 | Web Admin Panel
插件启动后，你可以通过浏览器直接访问管理面板进行全参数调节：

访问地址：
```bash
http://你的服务器IP:端口/aichat
```
(注：端口通常为 NoneBot 运行的端口，默认为 8080)





面板功能说明：
交互机制：调节触发前缀（如 #）及随机回复概率。

API 配置：设置 DeepSeek API Key 及端点。

模型参数：精细化调节 Temperature、Top_P 等生成参数。

身份映射：将复杂的 QQ 号映射为直观的角色昵称。





 配置项 | Configuration
插件会在 data/nonebot_plugin_aichat/ 目录下自动生成以下文件：

config.json: 存储核心配置及 API 信息。

characters.json: 存储用户昵称映射。

groups.json: 存储群聊名称映射。

memory.json: 存储长期记忆库。

[!TIP] 默认参数提示：面板中预设的 Prompt 和参数经过多次角色扮演测试，建议初次使用时参考默认值进行微调。

 
 
 
 注意事项 | Notice
隐私安全：请勿将生成的 config.json 文件上传到 GitHub 等公共平台，防止 API Key 泄露。

DeepSeek API：目前仅支持 DeepSeek 官方 API 格式。

 开源协议 | License
本项目采用 MIT 协议开源。
