import os
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

os.environ["LANGCHAIN_PROJECT"] = "Agentic Decision Project"

load_dotenv()
llm = ChatMistralAI(model="mistral-small-2506")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def pro_agent_node(state: AgentState):
    print("\n--- 🏃 [NODE 1 ACTIVATED]: Agen Pro sedang berpikir... ---")
    
    system_prompt = (
        "Kamu adalah Analis Optimis. Berikan 3 keuntungan besar, peluang, "
        "atau poin positif dari ide yang diberikan oleh user. Jawab dengan singkat dan padat."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    
    return {"messages": [HumanMessage(content=f"PRO ANALYSIS:\n{response.content}")]}

def contra_agent_node(state: AgentState):
    print("\n--- 🏃 [NODE 2 ACTIVATED]: Agen Kontra sedang berpikir... ---")
    
    system_prompt = (
        "Kamu adalah Analis Risiko (Skeptis). Lihatlah ide user dan hasil analisis Agen Pro sebelumnya. "
        "Berikan 3 risiko terbesar, kelemahan, atau potensi kegagalan dari ide tersebut. Jawab dengan singkat dan padat."
    )
    
    inputs = [HumanMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(inputs)
    
    return {"messages": [HumanMessage(content=f"CONTRA ANALYSIS:\n{response.content}")]}

workflow = StateGraph(AgentState)

workflow.add_node("node_pro", pro_agent_node)
workflow.add_node("node_contra", contra_agent_node)

workflow.add_edge(START, "node_pro")
workflow.add_edge("node_pro", "node_contra")
workflow.add_edge("node_contra", END)

app = workflow.compile()

if __name__ == "__main__":
    user_idea = "liburan di rumah aja dan belajar ai atau jalan jalan dengan teman teman"
    print(f"💡 Ide User: '{user_idea}'")
    
    initial_state = {"messages": [HumanMessage(content=user_idea)]}
    
    final_output = app.invoke(initial_state)
    
    print("\n=================== HASIL AKHIR DISKUSI ===================")
    for msg in final_output["messages"]:
        print(f"\n{msg.content}")