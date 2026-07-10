import os
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

load_dotenv()
llm = ChatMistralAI(model="mistral-small-2506")

class RoomState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def presenter_node(state: RoomState):
    print("[Node: Presenter] Sedang berbicara di depan kelas...")
    
    system_prompt = (
        "Kamu adalah Angga, murid yang baru saja selesai presentasi di depan kelas. "
        "Kamu merasa sedikit gugup tapi mencoba tetap tenang dan membuka sesi tanya jawab. "
        "Gaya bicaramu santai khas anak SMA tapi tetap sopan di depan guru. "
        "Contoh: 'Oke teman-teman, itu tadi presentasi dari kelompok kami. Sekarang kami buka sesi tanya jawab ya. "
        "Silahkan kalau ada yang mau tanya, gak apa-apa kok kalau agak aneh atau simpel, santai aja.'"
        "Berikan respon satu paragraf saja yang natural."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="Angga_Presenter")]}

def audience_ambisius_node(state: RoomState):
    print("[Node: Audiens Ambisius] Sedang bisik-bisik / berpikir...")
    
    system_prompt = (
        "Kamu adalah Budi, murid teladan yang duduk di bangku depan. Kamu tipe yang kritis dan ambisius. "
        "Mendengar Angga membuka pertanyaan, kamu langsung membolak-balik buku catatanmu untuk mencari "
        "pertanyaan yang berbobot agar terlihat pintar di depan guru, sekaligus menantang materi Angga. "
        "Tuliskan apa yang kamu ucapkan atau bisikan ke teman sebelahmu dengan gaya anak sekolahan yang kompetitif."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="Budi_Audiens_Ambisius")]}

def audience_pasrah_node(state: RoomState):
    print("[Node: Audiens Pasrah] Sedang mengamati situasi...")
    
    system_prompt = (
        "Kamu adalah Dito, murid yang duduk di pojok belakang. Kamu tidak terlalu paham materinya "
        "dan hanya ingin sesi ini cepat selesai. Kamu memperhatikan kelas yang hening dan membatin "
        "atau berbisik: 'Duh, siapa nih yang mau bertanya? Cepetan napa biar cepat kelar kelasnya, laper mau ke kantin.'"
        "Gunakan gaya bahasa santai/slang murid sekolah yang jujur dan apa adanya."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="Dito_Audiens_Pojok_Belakang")]}

def teacher_node(state: RoomState):
    print("[Node: Guru] Memotong keheningan kelas...")
    
    system_prompt = (
        "Kamu adalah Pak Bambang, guru mapel yang sedang menilai di meja belakang. "
        "Melihat kelas sempat hening dan tidak ada yang mengacungkan tangan, kamu menurunkan kacamata, "
        "melihat ke sekeliling kelas, dan memberikan umpan pancingan agar murid aktif. "
        "Contoh: 'Ayo anak-anak, kok sepi? Yang bertanya atau menanggapi presentasi Angga hari ini, "
        "Bapak kasih nilai tambahan +10 untuk nilai tugas ya.' "
        "Gunakan wibawa seorang guru yang tegas tapi memotivasi."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="Pak_Bambang_Guru")]}

workflow = StateGraph(RoomState)

workflow.add_node("presenter", presenter_node)
workflow.add_node("audiens_ambisius", audience_ambisius_node)
workflow.add_node("audiens_pasrah", audience_pasrah_node)
workflow.add_node("guru", teacher_node)

workflow.add_edge(START, "presenter")
workflow.add_edge("presenter", "audiens_ambisius")
workflow.add_edge("audiens_ambisius", "audiens_pasrah")
workflow.add_edge("audiens_pasrah", "guru")
workflow.add_edge("guru", END)

app = workflow.compile()

if __name__ == "__main__":
    konteks_awal = "Suasana kelas XI-A setelah kelompok Angga selesai memaparkan materi sejarah."
    
    print(f"🎬 KONTEKS SITUASI: {konteks_awal}\n")
    print("="*60)
    print("🎭 TRANSKRIP SIMULASI DIALOG KELAS (CLEAN VIEW)")
    print("="*60)
    
    initial_state = {"messages": [HumanMessage(content=konteks_awal)]}
    final_output = app.invoke(initial_state)
    
    for msg in final_output["messages"][1:]:
        karakter = msg.name.replace("_", " ")
        print(f"\n🗣️  [{karakter}]:")
        print(f'   "{msg.content}"')
        print("-" * 40)