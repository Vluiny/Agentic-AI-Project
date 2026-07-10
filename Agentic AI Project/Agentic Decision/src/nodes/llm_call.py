# src/nodes/llm_call.py
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from src.state import DecisionState
from src.prompts.promptAI import (
    system_prompt_analytical, 
    system_prompt_humanist,
    system_prompt_resource,
    system_prompt_strategist,
    system_prompt_social,
    system_prompt_judge,
    system_prompt_ringan,
    prompt_pakai_tool,
    system_prompt_router_2
)
from src.tools import info_search, get_weather

load_dotenv()

tools = [info_search, get_weather]

llm_fast = ChatMistralAI(model="mistral-small-2506")
llm_large = ChatMistralAI(model="mistral-medium-2508")


ringan_react = create_react_agent(llm_fast, tools, prompt=system_prompt_ringan + prompt_pakai_tool,)
tools_luar_react = create_react_agent(llm_fast, tools, prompt=system_prompt_router_2 + prompt_pakai_tool,)



def tanya_ringan_node(state: DecisionState):
    print("ringan diakses")
    hasil = ringan_react.invoke({"messages": state["messages"]})
    return {"messages": [hasil["messages"][-1]]}

def tools_luar_node(state: DecisionState):
    print("tool luar diakses")
    hasil = tools_luar_react.invoke({"messages": state["messages"]})
    return {"messages": [hasil["messages"][-1]]}

def analytical_mind_node(state: DecisionState):
    inputs = [SystemMessage(content=system_prompt_analytical)] + state["messages"]
    response = llm_fast.invoke(inputs)
    return {"messages": [response]}

def humanist_node(state: DecisionState):
    inputs = [SystemMessage(content=system_prompt_humanist)] + state["messages"]
    response = llm_fast.invoke(inputs)
    return {"messages": [response]}

def resource_investor_node(state: DecisionState):
    inputs = [SystemMessage(content=system_prompt_resource)] + state["messages"]
    response = llm_fast.invoke(inputs)
    return {"messages": [response]}

def strategist_node(state: DecisionState):
    inputs = [SystemMessage(content=system_prompt_strategist)] + state["messages"]
    response = llm_fast.invoke(inputs)
    return {"messages": [response]}

def social_lens_node(state: DecisionState):
    inputs = [SystemMessage(content=system_prompt_social)] + state["messages"]
    response = llm_fast.invoke(inputs)
    return {"messages": [response]}





def judge_node(state: DecisionState):
    original_messages = state["messages"]
    laporan_agen = []
    
    for msg in original_messages:
        if msg.type == "ai" and ("SKOR_" in msg.content or "Analisis" in msg.content or "Sudut Pandang" in msg.content):
            laporan_agen.append(msg.content)
            
    teks_gabungan_laporan = "\n\n=== LAPORAN ANALYSIS DARI AGEN SPESIALIS ===\n\n" + "\n\n".join(laporan_agen)
    
    inputs = [
        SystemMessage(content=system_prompt_judge),
        HumanMessage(content=f"Berikut adalah laporan komprehensif dari 5 agen spesialis kami. Tolong sintesis seluruh data ini menjadi keputusan final sesuai format Telegram Anda:\n\n{teks_gabungan_laporan}")
    ]
    
    response = llm_large.invoke(inputs)
    return {"messages": [response]}