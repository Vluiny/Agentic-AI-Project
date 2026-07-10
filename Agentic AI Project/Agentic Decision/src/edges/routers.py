# src/edges/routers.py
from langchain_core.messages import SystemMessage
from langchain_mistralai import ChatMistralAI
from src.state import DecisionState
from src.prompts.promptAI import system_prompt_classification, system_prompt_router_2

llm_fast = ChatMistralAI(model="mistral-small-2506")

def input_classifier_router(state: DecisionState) -> str:

    user_message = state["messages"][-1].content
    system_prompt = system_prompt_classification

    messages = [SystemMessage(content=system_prompt), user_message]
    
    response = llm_fast.invoke(messages)
    decision = response.content.strip().upper()
    
    if "DILEMA" in decision:
        print("Input diklasifikasikan sebagai dilema, mengarahkan ke multi-agent.")
        return "ke_multi_agent"
    else:
        print("Input diklasifikasikan sebagai fast response, mengarahkan ke Tanya Ringan.")
        return "ke_fast_response"
    


def router_tool_luar(state: DecisionState) -> str:

    user_message = state["messages"][-1].content
    system_prompt = system_prompt_router_2

    messages = [SystemMessage(content=system_prompt), user_message]
    
    response = llm_fast.invoke(messages)
    decision = response.content.strip().upper()
    
    if "BUTUH_DATA_LUAR" in decision:
        print("Butuh data dari luar")
        return "BUTUH_DATA_LUAR"
    else:
        print("Tiddak butuh data dr luar")
        return "TANPA_DATA_LUAR"
