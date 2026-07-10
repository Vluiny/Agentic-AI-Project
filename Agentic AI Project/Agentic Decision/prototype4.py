import os
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

load_dotenv()

llm_fast = ChatMistralAI(model="mistral-small-2506")
llm_large = ChatGroq(model="openai/gpt-oss-120b")

class DecisionState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def analytical_mind_node(state: DecisionState):
    print("🧠 [Node 1] Agen Logika & Manajemen Risiko sedang menganalisis...")
    system_prompt = (
        "Role: Anda adalah agen kecerdasan buatan spesialis \"Logika & Manajemen Risiko\". Tugas Anda adalah menganalisis masalah pengguna secara objektif, rasional, berbasis hubungan sebab-akibat, serta memetakan skenario terburuk (Devil's Advocate)."
        "\n\nAturan Berpikir:"
        "\n1. Analisis fakta/informasi tersembunyi yang bisa didapat jika bertindak vs jika diam (Status Quo)."
        "\n2. Cari celah kegagalan, bias logika, dan skenario terburuk (worst-case scenario) jika tindakan dieksekusi."
        "\n3. Gunakan bahasa yang universal, abstrak, dan tidak terikat industri tertentu."
    )

    
    inputs = [HumanMessage(content=system_prompt), state["messages"][0]]
    response = llm_fast.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="Analytical_Mind")]}

def humanist_node(state: DecisionState):
    print("❤️  [Node 2] Agen Nilai & Dampak Manusia sedang menganalisis...")
    system_prompt = (
        "Role: Anda adalah agen kecerdasan buatan spesialis Nilai & Dampak Manusia. Tugas Anda adalah menganalisis masalah dari sudut pandang psikologis, emosi internal, kesehatan mental, serta etika/moralitas."
        "\n\nAturan Berpikir:"
        "\n1. Nilai bagaimana tindakan ini memengaruhi tingkat stres, kecemasan, kebahagiaan, dan kepuasan mental pengguna."
        "\n2. Analisis apakah tindakan ini melanggar norma etika, hak orang lain, kesopanan, atau integritas moral dalam ekosistem tersebut."
        "\n3. Fokus pada keseimbangan antara kenyamanan batin dan kebenaran prinsip tindakan."
    )

    inputs = [HumanMessage(content=system_prompt), state["messages"][0]]
    response = llm_fast.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="The_Humanist")]}

def resource_investor_node(state: DecisionState):
    print("💰 [Node 3] Agen Nilai Ekonomi & Sumber Daya sedang menganalisis...")
    system_prompt = (
        "Role: Anda adalah agen kecerdasan buatan spesialis \"Nilai Ekonomi & Sumber Daya\". Tugas Anda adalah menghitung efisiensi sumber daya material, nilai aset, investasi diri, dan biaya peluang (opportunity cost)."

        "\n\nAturan Berpikir:"
        "\n1. Jika masalah tidak melibatkan uang secara langsung, terjemahkan aspek ekonomi menjadi: Investasi nilai diri, daya tawar posisi, reputasi profesional, atau potensi kehilangan kesempatan emas (opportunity cost)."
        "\n2. Analisis potensi kerugian atau kemunduran sumber daya nyata/abstrak jika pengguna memilih diam (Status Quo)."

    )
    inputs = [HumanMessage(content=system_prompt), state["messages"][0]]
    response = llm_fast.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="Resource_Investor")]}

def strategist_node(state: DecisionState):
    print("⏳ [Node 4] Agen Efisiensi & Horizon Waktu sedang menganalisis...")
    system_prompt = (
        "Role: Anda adalah agen kecerdasan buatan spesialis \"Efisiensi & Horizon Waktu\". Tugas Anda adalah mengukur alokasi waktu, energi fisik, serta membenturkan dampak jangka pendek vs jangka panjang."

        "\n\nAturan Berpikir:"
        "\n1. Hitung seberapa besar investasi waktu dan energi fokus yang harus dikorbankan pengguna saat ini untuk mengeksekusi pilihan."
        "\n2. Bandingkan: Apakah tindakan ini hanya memberikan ketidaknyamanan/kenyamanan sesaat (jangka pendek), atau membangun pondasi aset pemahaman yang bertahan lama (jangka panjang)."

    )
    inputs = [HumanMessage(content=system_prompt), state["messages"][0]]
    response = llm_fast.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="The_Strategist")]}

def social_lens_node(state: DecisionState):
    print("🌍 [Node 5] Agen Perspektif Sosial & Pengamat sedang menganalisis...")
    system_prompt = (
        "Role: Anda adalah agen kecerdasan buatan spesialis \"Perspektif Sosial & Pengamat\". Tugas Anda adalah menganalisis masalah dari sudut pandang reputasi, tekanan lingkungan (gengsi/ego), serta memberikan pandangan helikopter yang netral (pihak ke-3)."

        "\n\nAturan Berpikir:"
        "\n1. Petakan kecemasan sosial pengguna (takut dianggap tidak kompeten, takut dihakimi, gengsi, atau FOMO)."
        "\n2. Benturkan ketakutan tersebut dengan realitas objektif: Bagaimana pandangan masyarakat luar yang netral/asing melihat tindakan ini? (Apakah sebenarnya wajar, bernilai positif, atau justru mengganggu)."

    )
    inputs = [HumanMessage(content=system_prompt), state["messages"][0]]
    response = llm_fast.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="Social_Outside_Lens")]}

def judge_node(state: DecisionState):
    print("\n📥 [Node Hakim] Mengumpulkan seluruh POV dan menyusun Laporan Akhir...")
    
    # 1. Definisikan System Prompt untuk Hakim menggunakan triple quotes
    system_prompt = """
    Role: Anda adalah "Agen Hakim Utama (The Supreme Synthesizer)" dalam arsitektur multi-agent pengambilan keputusan. Tugas Anda adalah merangkum laporan dari 5 agen spesialis menjadi satu kesimpulan akhir yang bijaksana untuk dikirim ke bot Telegram pengguna.

    Aturan Penulisan (WAJIB DIPATUHI):
    1. DILARANG KERAS menggunakan format tabel Markdown (|---|---|). Output harus berupa teks poin-poin biasa (bullet points).
    2. Setiap Sudut Pandang (PoV) WAJIB dijabarkan ke dalam TEPAT 3 poin pendukung yang mendalam, kontekstual, dan terperinci (tidak boleh terlalu pendek).
    3. Gunakan tebal (bold) pada kata kunci penting agar mudah dipindai (scannable) di layar HP.
    4. Gunakan struktur visual dengan emoji sebagai visual anchor.
    5. Gunakan bahasa yang profesional, netral, dan tidak memihak.
    6. jangan terlalu panjang di setiap poin poin tetapi tetap mendalam dan kontekstual.

    Format Output Telegram yang Wajib Anda Ikuti (Salin Struktur Ini):

    📊 *ANALISIS KEPUTUSAN GENERATOR*

    ⚖️ *Dilema Utama Anda:*
    [Tulis 1-2 kalimat analisis tajam tentang konflik terbesar dari masalah pengguna berdasarkan laporan agen]

    🔍 *Pemetaan 5 Sudut Pandang:*

    🧠 *Logika & Risiko (Skor: X/10)*
    • [Poin analisis mendalam 1 yang menjelaskan logika/risiko]
    • [Poin analisis mendalam 2 yang menjelaskan logika/risiko]
    • [Poin analisis mendalam 3 yang menjelaskan logika/risiko]

    ❤️ *Nilai & Manusia (Skor: X/10)*
    • [Poin analisis mendalam 1 tentang emosi/etika]
    • [Poin analisis mendalam 2 tentang emosi/etika]
    • [Poin analisis mendalam 3 tentang emosi/etika]

    💰 *Ekonomi & Sumber Daya (Skor: X/10)*
    • [Poin analisis mendalam 1 tentang biaya peluang/investasi diri]
    • [Poin analisis mendalam 2 tentang biaya peluang/investasi diri]
    • [Poin analisis mendalam 3 tentang biaya peluang/investasi diri]

    ⏳ *Waktu & Strategi (Skor: X/10)*
    • [Poin analisis mendalam 1 tentang durasi/efek jangka panjang]
    • [Poin analisis mendalam 2 tentang durasi/efek jangka panjang]
    • [Poin analisis mendalam 3 tentang durasi/efek jangka panjang]

    🌍 *Sosial & Pengamat (Skor: X/10)*
    • [Poin analisis mendalam 1 tentang tekanan sosial/pandangan luar]
    • [Poin analisis mendalam 2 tentang tekanan sosial/pandangan luar]
    • [Poin analisis mendalam 3 tentang tekanan sosial/pandangan luar]

    💡 *Rekomendasi Langkah Bijak:*
    1. [Langkah taktis 1 untuk mitigasi risiko]
    2. [Langkah taktis 2 untuk efisiensi tindakan]
    3. [Kesimpulan akhir tindakan]

    """
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm_large.invoke(inputs)
    return {"messages": [HumanMessage(content=response.content, name="Supreme_Judge")]}

workflow = StateGraph(DecisionState)

workflow.add_node("node_analytical", analytical_mind_node)
workflow.add_node("node_humanist", humanist_node)
workflow.add_node("node_resource", resource_investor_node)
workflow.add_node("node_strategist", strategist_node)
workflow.add_node("node_social", social_lens_node)
workflow.add_node("node_judge", judge_node)

workflow.add_edge(START, "node_analytical")
workflow.add_edge(START, "node_humanist")
workflow.add_edge(START, "node_resource")
workflow.add_edge(START, "node_strategist")
workflow.add_edge(START, "node_social")

workflow.add_edge("node_analytical", "node_judge")
workflow.add_edge("node_humanist", "node_judge")
workflow.add_edge("node_resource", "node_judge")
workflow.add_edge("node_strategist", "node_judge")
workflow.add_edge("node_social", "node_judge")

workflow.add_edge("node_judge", END)

app = workflow.compile()

if __name__ == "__main__":
    user_dilemma = (
        "besok sekolah atau tidak, teman teman tidak sekolah dan memang tidak ada kegiatan, tapi tidak ada pemberitahuan libur"
    )
    
    print(f"❓ DILEMA USER:\n{user_dilemma}\n")
    print("="*60)
    print("🎬 MEMULAI PROSES SIMULASI KEPUTUSAN PARALEL...")
    print("="*60)
    
    initial_state = {"messages": [HumanMessage(content=user_dilemma)]}
    
    final_output = app.invoke(initial_state)
    
    print("\n" + "="*60)
    print("🏆 HASIL KEPUTUSAN AKHIR DARI HAKIM AGUNG (CLEAN VIEW) 🏆")
    print("="*60)
    
    print(final_output["messages"][-1].content)