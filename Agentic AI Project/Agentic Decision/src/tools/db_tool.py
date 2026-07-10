# src/tools/db_tool.py
import os
from supabase import create_client, Client
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_chat_history(user_id: str, limit: int = 5):
    """Mengambil riwayat obrolan langsung dari kolom message Supabase."""
    try:
        response = supabase.table("chatbot_history") \
            .select("message") \
            .eq("user_id", user_id) \
            .order("timestamp", desc=True) \
            .limit(limit) \
            .execute()
        
        langchain_messages = []
        
        
        records = reversed(response.data)
        
        for record in records:
            full_text = record["message"]
            
            
            if " Jawaban :" in full_text:
                parts = full_text.split(" Jawaban :", 1)
                user_part = parts[0].replace("Pertanyaan :", "").strip()
                ai_part = parts[1].strip()
                
                langchain_messages.append(HumanMessage(content=user_part))
                langchain_messages.append(AIMessage(content=ai_part))
                
        return langchain_messages
    except Exception as e:
        print(f"⚠️ Gagal memuat history: {e}")
        return []

def save_chat_history(user_id: str, user_text: str, ai_reply: str):
    """Menyimpan input user dan output bot ke kolom message."""
    try:
        
        formatted_message = f"Pertanyaan :{user_text} Jawaban :{ai_reply}"
        
        data = {
            "user_id": user_id,
            "message": formatted_message
        }
        
        supabase.table("chatbot_history").insert(data).execute()
        print(f"💾 Terinput ke Supabase untuk Telegram ID: {user_id}")
    except Exception as e:
        print(f"⚠️ Gagal menyimpan ke Supabase: {e}")
