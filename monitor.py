import asyncio
import logging
import pytz
import re
import os
from datetime import datetime
from pyrogram import Client, filters
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ================= 从环境变量获取配置 =================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_PERSONAL_ID = int(os.getenv("MY_PERSONAL_ID"))

# 监控配置 (也可移至环境变量)
FORCE_POLL_CHATS = [-1002565053719] 
TARGET_USERS = ["eoocen"]
TARGET_UIDS = [6018078561]
CHECKIN_TIME = "10:00"

# 关键词库
LUCKY_KEYWORDS = ['抽奖', '参与关键词', '参与口令', 'lucky', '奖品', '口令：']
RESULT_WORDS = ["抽奖结果", "中奖名单", "已结束"]

# 自动签到任务
SIGN_TASKS = [
    {"name": "Navidrome", "user": "@navidrome_bot", "type": "button", "cmd": "/start", "btn": "签到"},
    {"name": "ICMP9", "user": "@ICMP9_Bot", "type": "button", "cmd": "/start", "btn": "📅 签到"},
    # ... 其他任务 ...
]

# ================= 屏蔽词管理 =================
SPAM_FILE = "spam_words.txt"

def load_spam_words():
    if not os.path.exists(SPAM_FILE):
        return []
    with open(SPAM_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_spam_word(new_word):
    words = load_spam_words()
    if new_word not in words:
        with open(SPAM_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{new_word}")
        return True
    return False

SPAM_WORDS = load_spam_words()

# ================= 程序核心 =================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Client("my_account_session", api_id=API_ID, api_hash=API_HASH, workdir="./")
bot_app = Client("my_bot_notifier", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, workdir="./")

last_processed_ids = {}

@app.on_message(filters.me & filters.regex(r"^/add_spam "))
async def add_spam_command(client, message):
    new_word = message.text.replace("/add_spam ", "").strip()
    if not new_word: return
    if save_spam_word(new_word):
        SPAM_WORDS.append(new_word)
        await message.edit(f"✅ 已永久添加屏蔽词：`{new_word}`\n词库总数：{len(SPAM_WORDS)}")
    else:
        await message.edit(f"ℹ️ `{new_word}` 已在屏蔽名单中。")

async def process_msg(message):
    try:
        content = (message.text or message.caption or "").strip()
        if not content or any(s in content for s in SPAM_WORDS): return

        sender = message.from_user
        sender_chat = message.sender_chat
        display_name = "未知发送者"
        un, uid = "", 0

        if sender:
            display_name = f"@{sender.username}" if sender.username else (sender.first_name or "用户")
            un, uid = (sender.username or "").lower(), sender.id
        elif sender_chat:
            display_name = f"📢 {sender_chat.title}"
            un, uid = (sender_chat.username or "").lower(), sender_chat.id

        is_target = (un in [n.lower() for n in TARGET_USERS] or uid in TARGET_UIDS)
        is_lucky = any(k in content for k in LUCKY_KEYWORDS)
        is_result = any(r in content for r in RESULT_WORDS)

        if (is_target or is_lucky or is_result):
            chat_id = message.chat.id
            link = f"https://t.me/c/{str(chat_id).replace('-100', '')}/{message.id}"
            group_name = message.chat.title or "未知群组"
            
            tag = "🗣️ 重点人" if is_target else ("🎰 抽奖" if is_lucky else "📢 结果")
            header = f"{tag} | **{display_name}** ({group_name})"
            final_msg = f"{header}\n\n{content}\n\n🔗 [跳转直达]({link})"
            
            await bot_app.send_message(MY_PERSONAL_ID, final_msg, disable_web_page_preview=True)
    except Exception as e:
        logging.error(f"Error: {e}")

# ... (polling_worker, scheduler, run_checkin 函数保持不变) ...

async def main():
    async with app, bot_app:
        async for dialog in app.get_dialogs():
            if dialog.chat.type.value in ["supergroup", "group"]:
                last_processed_ids[dialog.chat.id] = dialog.top_message.id if dialog.top_message else 0
        logging.info(f"🚀 监控系统已启动！")
        await asyncio.gather(polling_worker(), scheduler(), asyncio.Event().wait())

if __name__ == "__main__":
    app.run(main())
