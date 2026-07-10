import os
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

load_dotenv()
llm = ChatMistralAI(model="mistral-small-2506")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def pro_agent_initial_node(state: AgentState):
    print("\n[PRO - Langkah 1]: Menganalisis potensi dan peluang emas...")
    
    system_prompt = (
        "Kamu adalah Analis Senior rumpun Komersial dan Bisnis (Optimis). "
        "Tugasmu adalah menganalisis ide user dan membeberkan potensi keuntungan terbesar, "
        "strategi monetisasi, daya tarik pasar, dan mengapa ide ini LAYAK dijalankan. "
        "Berikan argumen yang kuat berbasis logika bisnis yang matang."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    
    return {"messages": [HumanMessage(content=f"📌 [ANALISIS PRO - PELUANG]:\n{response.content}", name="Pro_Agent")]}

def contra_agent_node(state: AgentState):
    print("\n[KONTRA]: Mencari celah, kelemahan, dan risiko fatal...")
    
    system_prompt = (
        "Kamu adalah Analis Risiko Senior dan Auditor Bisnis (Skeptis/Kritis). "
        "Tugasmu adalah membedah ide user DAN menyanggah argumen dari Agen Pro sebelumnya. "
        "Beberkan risiko operasional, ancaman kompetitor, potensi kerugian finansial, "
        "dan blind-spot yang diabaikan oleh Agen Pro. Bersikaplah sangat kritis dan tajam."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    
    return {"messages": [HumanMessage(content=f"⚠️ [ANALISIS KONTRA - SANGGAHAN RISIKO]:\n{response.content}", name="Contra_Agent")]}

def pro_agent_rebuttal_node(state: AgentState):
    print("\n[PRO - Langkah 2]: Menyusun counter-argument dan mitigasi risiko...")
    
    system_prompt = (
        "Kamu kembali sebagai Analis Bisnis (Optimis). "
        "Kamu telah mendengar serangan risiko dari Agen Kontra. "
        "Tugasmu sekarang BUKAN mengulang argumen pertama, melainkan memberikan JAWABAN atau "
        "solusi mitigasi terhadap risiko yang disebutkan Agen Kontra tadi. "
        "Buktikan bahwa risiko-risiko tersebut bisa diatasi dengan strategi yang tepat."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    
    return {"messages": [HumanMessage(content=f"⚡ [RESPONS PRO - MITIGASI]:\n{response.content}", name="Pro_Agent_Rebuttal")]}

def synthesizer_node(state: AgentState):
    print("\n[SINTESIS - REVIEWER]: Menyusun laporan keputusan akhir yang matang...")
    
    system_prompt = (
        "Kamu adalah Ketua Dewan Direksi / Konsultan Bisnis Utama yang objektif dan bijaksana. "
        "Tugasmu adalah meninjau seluruh jalannya debat antara Agen Pro dan Agen Kontra dari awal sampai akhir. "
        "Buatlah satu Laporan Eksklusif Akhir (Executive Summary) yang berisi:\n"
        "1. Penilaian Objektif terhadap ide ini.\n"
        "2. Poin Pro vs Kontra yang paling valid.\n"
        "3. Keputusan Final: Apakah ide ini Layak Jalan (Go), Layak dengan Syarat/Pivot (Pivot), atau Tolak (No-Go).\n"
        "4. Langkah strategis konkret yang harus diambil user sebagai pondasi awal.\n"
        "Gunakan bahasa profesional, terstruktur, dan sangat matang."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    
    return {"messages": [HumanMessage(content=f"🏆 [LAPORAN KEPUTUSAN AKHIR]:\n{response.content}", name="Synthesizer")]}

workflow = StateGraph(AgentState)

workflow.add_node("node_pro_initial", pro_agent_initial_node)
workflow.add_node("node_contra", contra_agent_node)
workflow.add_node("node_pro_rebuttal", pro_agent_rebuttal_node)
workflow.add_node("node_synthesizer", synthesizer_node)

workflow.add_edge(START, "node_pro_initial")
workflow.add_edge("node_pro_initial", "node_contra")
workflow.add_edge("node_contra", "node_pro_rebuttal")
workflow.add_edge("node_pro_rebuttal", "node_synthesizer")
workflow.add_edge("node_synthesizer", END)

app = workflow.compile()

if __name__ == "__main__":
    user_idea = (
        "ikut jalan jalan ke jogja bareng teman atau belajar di rumah aja sambil belajar AI dan coding."
    )
    
    print(f"💡 IDE STRATEGIS USER:\n{user_idea}\n")
    print("🤖 Memulai Proses Debat Tingkat Tinggi & Penyusunan Laporan Matang...")
    
    initial_state = {"messages": [HumanMessage(content=user_idea)]}
    
    final_output = app.invoke(initial_state)
    
    print("\n" + "="*40)
    print("🔥 PROSES DEBAT SELESAI. BERIKUT LAPORAN AKHIR: 🔥")
    print("="*40)
    
    print(final_output["messages"][-1].content)