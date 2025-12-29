# Telegram Group Monitor & Notifier

这是一个基于 Pyrogram 开发的 Telegram 监控脚本。它能使用个人账号监控指定群组中的关键词（如抽奖、重点人发言），并通过机器人（Bot）主动向你发送弹窗通知。

## ✨ 功能特性
- **双模运行**：User Client 负责群组监控，Bot Client 负责私聊推送（确保手机弹窗提醒）。
- **关键词监控**：实时扫描抽奖信息、中奖结果或特定用户发言。
- **动态屏蔽词**：支持通过指令 `/add_spam` 实时添加屏蔽词并本地持久化。
- **自动签到**：内置定时任务，支持按钮点击类和文本指令类机器人签到。

## 🚀 快速开始

### 1. 获取 API
前往 [my.telegram.org](https://my.telegram.org) 获取你的 `API_ID` 和 `API_HASH`。
通过 [@BotFather](https://t.me/BotFather) 创建一个机器人并获取 `BOT_TOKEN`。

### 2. 环境准备
```bash
pip install pyrogram tgcrypto python-dotenv pytz
### 3. 配置
创建 .env 文件，填入你的配置信息（参考 .env.example）：
API_ID=123456
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
MY_PERSONAL_ID=你的数字ID
### 4. 运行
python monitor.py
