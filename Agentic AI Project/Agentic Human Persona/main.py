from langchain_core.messages import HumanMessage
import json
from src.agent import app
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
from src.tools.db_tool import save_chat_history, get_chat_history

load_dotenv()

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    user_text = update.message.text

    chat_history = get_chat_history(user_id=chat_id, limit=20)

    if len(chat_history) > 20:
        chat_history = chat_history[-20:]
    
    input_message = HumanMessage(content=user_text)
    full_messages = chat_history + [input_message]

    result = app.invoke({"messages": full_messages})
    # reply = result["messages"][-1].content
    raw_reply = result["messages"][-1].content

    # Jika Gemini mengembalikan string berupa list JSON bawaan

    # 1. Pastikan bentuknya sudah jadi dictionary Python (bukan string)
    if isinstance(raw_reply, str):
        try: raw_reply = json.loads(raw_reply)
        except: pass

    # 2. Langsung ambil teksnya
    try:
        # Akses langsung: messages -> index 1 (AI) -> content -> index 0 -> text
        reply = raw_reply["messages"][1]["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        # Fallback jika strukturnya tiba-tiba berbeda (misal cuma string biasa)
        reply = str(raw_reply)

        save_chat_history(user_id=chat_id, user_text=user_text, ai_reply=reply)
        await update.message.reply_text(reply)

application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot Telegram berjalan...")
application.run_polling()