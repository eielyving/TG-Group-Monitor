# 🎰 Telegram 监控与自动签到助手

这是一个基于 Pyrogram 的双模监控系统。它使用个人账号监控群聊，并通过 Bot 发送私聊通知。且具有自动定时签到功能。完善中

## 📂 项目结构

```text
TG-Group-Monitor/
├── .env                # (私有) 存放你的 API_ID 和 Token
├── .env.example        # (公开) 配置模板，供他人参考
├── .gitignore          # (公开) 告诉 GitHub 忽略哪些隐私文件
├── monitor.py          # (公开) 主程序代码
├── spam_words.txt      # (公开) 存放屏蔽词的文件
└── README.md           # (公开) 项目说明文档
```

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
在终端执行以下命令安装依赖：
```bash
pip install pyrogram tgcrypto python-dotenv pytz
```

### 3. 配置环境变量
创建一个名为 .env 的文件（可以参考 .env.example），内容如下：
```bash
API_ID=30271473
API_HASH=1d349a66cf916848f92018acc04cb09c
BOT_TOKEN=你的机器人TOKEN
MY_PERSONAL_ID=6753706885
```
### 4. 运行程序
第一次启动需要输入手机号验证码登录个人账号
```bash
python3 monitor.py
```

## 🛠️ 功能说明

屏蔽词动态维护
你可以在 Telegram 的任何聊天窗口（如“收藏夹”）发送以下指令：

```/add_spam``` 关键词：实时将该词加入屏蔽名单，并自动保存到 ```spam_words.txt```。


```SIGN_TASKS```修改说明:

如果想修改签到任务，需要手动编辑 ```monitor.py``` 文件中的 ```SIGN_TASKS``` 列表

监控逻辑
- 重点用户：实时追踪特定 UID 的发言。

- 抽奖词库：自动识别群聊中的抽奖口令、参与方式。

- 自动签到：每日 10:00 自动执行预设的机器人签到任务。

⚠️ 安全提醒
- 请勿上传 .env 和 .session 文件到公开仓库！

- 本项目仅供学习交流使用。
