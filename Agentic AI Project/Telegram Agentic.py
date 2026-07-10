from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
from AgenticAI import app
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    input_message = HumanMessage(content=user_text)

    config = {"configurable": {"thread_id": str(chat_id)}}
    
    result = app.invoke(
        {
            "messages": [input_message]
        },
        config=config
    )

    reply = result["messages"][-1].content

    await update.message.reply_text(reply)

application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot Telegram berjalan...")
application.run_polling()