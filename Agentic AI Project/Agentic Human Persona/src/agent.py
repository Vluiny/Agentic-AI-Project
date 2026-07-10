from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.node.call_llm import tanya_ringan_node


workflow = StateGraph(AgentState)

workflow.add_node("tanya_ringan", tanya_ringan_node)

workflow.set_entry_point("tanya_ringan")
workflow.add_edge("tanya_ringan", END)

app = workflow.compile()