from typing import List, Union
from core.constants import MAX_REFLECTION_REVISIONS
from core.logger import logger

def planner_fanout_router(state: dict) -> List[str]:
    """
    Returns parallel branches (research, technical, news) based on planner execution_plan.
    Enables parallel execution of data collection nodes in LangGraph.
    """
    plan = state.get("execution_plan", [])
    branches = []

    for step in ["research", "technical", "news"]:
        if step in plan:
            branches.append(step)

    if not branches:
        branches.append("report")

    logger.info(f"Planner fanout scheduling parallel branches: {branches}")
    return branches

def post_report_router(state: dict) -> str:
    """
    Determines next step after report node (reflection, critic, or END).
    """
    plan = state.get("execution_plan", [])

    if "reflection" in plan and "reflection" not in state.get("timings", {}):
        return "reflection"
    elif "critic" in plan and "critic" not in state.get("timings", {}):
        return "critic"
    else:
        return "END"

def reflection_router(state: dict) -> str:
    """
    Checks if reflection, critic, or human feedback requested a report revision.
    """
    plan = state.get("execution_plan", [])
    reflection = state.get("reflection", {})
    critic = state.get("critic", {})
    revisions = state.get("revision_count", 0)

    # Next node if no revision needed
    next_node = "critic" if ("critic" in plan and "critic" not in state.get("timings", {})) else "END"

    needs_revision = (
        reflection.get("status") == "NEEDS_REVISION" or
        critic.get("status") == "REJECTED" or
        state.get("human_approved") is False
    )

    if needs_revision and revisions < MAX_REFLECTION_REVISIONS:
        logger.info(f"Revision requested (Attempt {revisions + 1}). Routing back to 'report'.")
        return "report"

    return next_node
