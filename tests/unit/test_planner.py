import pytest
from agents.planner_agent import planner_agent

def test_planner_agent():
    request = "Analyze Apple and Microsoft fundamentals and technicals"
    plan = planner_agent(request)
    assert isinstance(plan, dict)
    assert "companies" in plan
    assert "execution_plan" in plan
    assert "report" in plan["execution_plan"]
