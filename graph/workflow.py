from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes import (
    planner_node,
    research_node,
    technical_node,
    news_node,
    report_node,
    reflection_node,
    critic_node,
)
from graph.router import planner_fanout_router, post_report_router, reflection_router

# Initialize State Graph
workflow = StateGraph(GraphState)

# Add all nodes
workflow.add_node("planner", planner_node)
workflow.add_node("research", research_node)
workflow.add_node("technical", technical_node)
workflow.add_node("news", news_node)
workflow.add_node("report", report_node)
workflow.add_node("reflection", reflection_node)
workflow.add_node("critic", critic_node)

# Set Entry Point
workflow.set_entry_point("planner")

# Parallel Fan-Out Edges from Planner
workflow.add_conditional_edges(
    "planner",
    planner_fanout_router,
    {
        "research": "research",
        "technical": "technical",
        "news": "news",
        "report": "report",
    }
)

# Fan-In Convergence to Report
workflow.add_edge("research", "report")
workflow.add_edge("technical", "report")
workflow.add_edge("news", "report")

# Post-Report Routing (Reflection, Critic, or END)
workflow.add_conditional_edges(
    "report",
    post_report_router,
    {
        "reflection": "reflection",
        "critic": "critic",
        "END": END,
    }
)

# Reflection & Critic Routing with Revision Loops
workflow.add_conditional_edges(
    "reflection",
    reflection_router,
    {
        "report": "report",
        "critic": "critic",
        "END": END,
    }
)

workflow.add_conditional_edges(
    "critic",
    reflection_router,
    {
        "report": "report",
        "critic": "critic",
        "END": END,
    }
)

# Compile Graph
graph = workflow.compile()