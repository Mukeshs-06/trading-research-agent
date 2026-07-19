import pytest
from graph.workflow import graph

def test_full_workflow_execution():
    initial_state = {
        "user_request": "Compare Apple stock fundamentals",
        "companies": [],
        "execution_plan": [],
        "current_step": 0,
        "execution_trace": [],
        "timings": {},
        "errors": [],
    }

    final_state = graph.invoke(initial_state)

    assert "report" in final_state
    assert len(final_state.get("report", "")) > 0
    assert "execution_trace" in final_state
    assert len(final_state["execution_trace"]) > 0
