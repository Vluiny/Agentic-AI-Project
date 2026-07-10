import os
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage  


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Tavily Agent Project"

load_dotenv() 

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

tavily_tool = TavilySearch(max_results=3)
tools = [tavily_tool]

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
).bind_tools(tools)


def agent_node(state: AgentState):

    system_instruction = SystemMessage(
        content=(
            "Anda adalah asisten AI yang ramah dan cerdas. "
            "Gunakan tool 'tavily_search' HANYA JIKA pengguna menanyakan informasi terkini, "
            "berita terbaru, atau data fakta spesifik yang tidak Anda ketahui. "
            "Untuk sapaan (halo, hai), obrolan ringan, pertanyaan tentang kemampuan Anda (seperti bisa bahasa Indonesia atau tidak), "
            "atau pertanyaan logika/matematika sederhana, JAWABLAH LANGSUNG secara alami tanpa menggunakan tool sama sekali."
        )
    )
    
    input_messages = [system_instruction] + list(state["messages"])
    
    response = model.invoke(input_messages)
    return {"messages": [response]}


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return "end"

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
tool_node = ToolNode(tools)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", "end": END}
)

workflow.add_edge("tools", "agent")


memory = MemorySaver()

app = workflow.compile(checkpointer=memory)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "test_lokal"}}
    query = "What is the latest news about AI?"
    result = app.invoke({"messages": [HumanMessage(content=query)]}, config=config)
    print(result["messages"][-1].content)