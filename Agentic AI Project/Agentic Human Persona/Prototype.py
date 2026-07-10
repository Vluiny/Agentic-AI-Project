from typing import TypedDict, Annotated, Sequence
from operator import add
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

# Initialize Model (Menggunakan Llama 4 Scout via Groq)
llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add] # Menggunakan BaseMessage agar kompatibel dengan model.invoke
    user_emotion: str                        
    persona_profile: dict                    
    draft_response: str                      
    final_response: str                      

# 2. Define Nodes dengan LLM Invoke
def analyze_emotion_node(state: AgentState):
    """Menganalisis emosi user dari pesan terakhir."""
    last_message = state["messages"][-1].content
    
    prompt = f"""Analisis emosi dari pesan berikut secara sangat singkat. 
Cukup berikan 1 kata label emosi utama (misal: Frustrasi, Senang, Bingung, Netral).

Pesan: '{last_message}'
Label Emosi:"""
    
    response = llm.invoke(prompt)
    # Ambil konten teks bersih dari response
    emotion = response.content.strip()
    
    return {"user_emotion": emotion}

def generate_response_node(state: AgentState):
    """Membuat draf respons dasar berdasarkan persona dan emosi user."""
    persona = state["persona_profile"]
    emotion = state["user_emotion"]
    messages = state["messages"]
    
    system_prompt = f"""Kamu adalah AI dengan persona manusia nyata berikut:
- Nama & Sifat: {persona['name']} - {persona['traits']}
- Gaya Bicara: {persona['tone']}

Kondisi psikologis user saat ini sedang: {emotion}. 
Tanggapi pesan user dengan empati yang sangat sesuai dengan persona kamu. Jangan sebutkan label emosi secara eksplisit dalam obrolan."""
    
    # Gabungkan SystemMessage dengan history chat (messages)
    full_messages = [SystemMessage(content=system_prompt)] + list(messages)
    
    response = llm.invoke(full_messages)
    
    return {"draft_response": response.content}

def refine_voice_node(state: AgentState):
    """Memoles draf agar terdengar 100% natural, manusiawi, dan tidak kaku."""
    draft = state["draft_response"]
    persona = state["persona_profile"]
    
    refine_prompt = f"""Ubah teks draf di bawah ini agar terdengar 100% natural seperti manusia asli yang sedang mengobrol santai ({persona['tone']}).
Hapus sapaan template AI yang berulang, jangan terlalu kaku, dan pastikan mengalir layaknya ketikan di chat aplikasi.

Draf Asli:
"{draft}"

Hasil Polish/Refine (Hanya keluarkan teks chat akhirnya saja):"""
    
    response = llm.invoke(refine_prompt)
    
    return {"final_response": response.content}

# 3. Build Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("analyze_emotion", analyze_emotion_node)
workflow.add_node("generate_response", generate_response_node)
workflow.add_node("refine_voice", refine_voice_node)

# Set Entry Point & Edges
workflow.set_entry_point("analyze_emotion")
workflow.add_edge("analyze_emotion", "generate_response")
workflow.add_edge("generate_response", "refine_voice")
workflow.add_edge("refine_voice", END)

# Compile Graph
app = workflow.compile()

# 4. Run & Test Prototype
initial_input = {
    "messages": [HumanMessage(content="Gak ngerti lagi deh, ini sistemnya error terus dari tadi pagi!")],
    "persona_profile": {
        "name": "Alex",
        "traits": "Sabar, solutif, santai tapi profesional",
        "tone": "Bahasa Indonesia kasual, gunakan partikel 'ya', 'sih', 'kok', hindari kata kaku seperti 'Anda' atau 'Maaf atas ketidaknyamanannya'."
    }
}

print("--- Memulai Eksekusi Graf ---\n")
for output in app.stream(initial_input):
    for key, value in output.items():
        print(f"[{key.upper()}] selesai.")
        # Mari kita intip apa saja isi state yang berubah di setiap node
        if "user_emotion" in value:
            print(f" -> Emosi Terdeteksi: {value['user_emotion']}")
        if "draft_response" in value:
            print(f" -> Draft: {value['draft_response']}")
        if "final_response" in value:
            print(f"\n-> HASIL AKHIR (Refined Voice):\n{value['final_response']}")
        print("-" * 30)