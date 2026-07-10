
# ============================================================================

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from src.agent import app
from langchain_core.messages import HumanMessage, SystemMessage
from src.tools.db_tool import get_chat_history, save_chat_history
import os
from dotenv import load_dotenv
from src.prompts.promptAI import system_prompt_routing
from src.nodes.llm_call import llm_fast

load_dotenv()

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text
    
    chat_history = get_chat_history(str(chat_id))
    
    if len(chat_history) > 20:
        chat_history = chat_history[-20:]
    
    routing_messages = [
        SystemMessage(content=system_prompt_routing),
        HumanMessage(content=user_text)
    ]
    classification = llm_fast.invoke(routing_messages).content.strip()
    
    if "MASALAH_BARU" in classification:
        history_for_invoke = [msg for msg in chat_history if not (msg.type == "ai" and "ANALISIS KEPUTUSAN" in getattr(msg, "content", ""))]
        print("--- [JALUR DILEMA BARU]: Memori Analisis Lama Dibersihkan ---")
    else:
        history_for_invoke = chat_history.copy()
        print("--- [JALUR CHAT/DISKUSI SANTAI]: Semua Log Dibawa ---")
    
    history_for_invoke.append(HumanMessage(content=user_text))
    
    result = app.invoke({"messages": history_for_invoke})
    reply = result["messages"][-1].content
    
    save_chat_history(str(chat_id), user_text, reply)
    
    try:
        await update.message.reply_text(reply, parse_mode="Markdown")
    except:
        await update.message.reply_text(reply)

application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot Telegram berjalan...")
application.run_polling()