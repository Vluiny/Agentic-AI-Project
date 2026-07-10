# agent.py
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from src.tools import info_search, get_weather
from src.state import DecisionState
from src.nodes.llm_call import (
    analytical_mind_node, humanist_node, resource_investor_node,
    strategist_node, social_lens_node, judge_node, tanya_ringan_node, tools_luar_node
)
from src.edges.routers import input_classifier_router, router_tool_luar

workflow = StateGraph(DecisionState)

workflow.add_node("node_analytical", analytical_mind_node)
workflow.add_node("node_humanist", humanist_node)
workflow.add_node("node_resource", resource_investor_node)
workflow.add_node("node_strategist", strategist_node)
workflow.add_node("node_social", social_lens_node)
workflow.add_node("node_judge", judge_node)
workflow.add_node("node_tanya_ringan", tanya_ringan_node)
workflow.add_node("node_tool_luar", tools_luar_node)


workflow.add_node("tools", ToolNode([info_search, get_weather]))

workflow.add_node("node_routing_dilema", lambda state: state)
workflow.add_node("node_routing_tool", lambda state: state)

workflow.add_conditional_edges(
    START,
    input_classifier_router,
    {
        "ke_fast_response": "node_tanya_ringan",
        "ke_multi_agent": "node_routing_tool"
    }
)

workflow.add_conditional_edges(
    "node_routing_tool",
    router_tool_luar,
    {
        "BUTUH_DATA_LUAR" : "node_tool_luar",
        "TANPA_DATA_LUAR" : "node_routing_dilema"
    }
)

workflow.add_edge("node_tool_luar", "node_routing_dilema")

# Sebar paralel dari node perantara ke 5 agen
workflow.add_edge("node_routing_dilema", "node_analytical")
workflow.add_edge("node_routing_dilema", "node_humanist")
workflow.add_edge("node_routing_dilema", "node_resource")
workflow.add_edge("node_routing_dilema", "node_strategist")
workflow.add_edge("node_routing_dilema", "node_social")

workflow.add_edge("node_analytical", "node_judge")
workflow.add_edge("node_humanist", "node_judge")
workflow.add_edge("node_resource", "node_judge")
workflow.add_edge("node_strategist", "node_judge")
workflow.add_edge("node_social", "node_judge")

workflow.add_edge("node_tanya_ringan", END)
workflow.add_edge("node_judge", END)

app = workflow.compile()