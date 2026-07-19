import json
import re
from langchain_core.messages import SystemMessage, HumanMessage
from core.settings import llm
from core.logger import logger
from prompts.planner_prompt import PLANNER_PROMPT

def planner_agent(user_request: str) -> dict:
    """
    Parses user request and returns an execution plan dict.
    Returns:
    {
       "companies": [...],
       "execution_plan": [...]
    }
    """
    logger.info(f"Planner Agent processing request: '{user_request}'")
    try:
        response = llm.invoke([
            SystemMessage(content=PLANNER_PROMPT),
            HumanMessage(content=user_request),
        ])
        content = response.content.strip()

        # Clean markdown code blocks if LLM included them
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\n?", "", content)
            content = re.sub(r"\n?```$", "", content).strip()

        plan = json.loads(content)

        # Basic validations
        companies = plan.get("companies", [])
        execution_plan = plan.get("execution_plan", plan.get("agents", []))

        if not companies:
            companies = ["Apple"] # Default fallback if none detected

        if not execution_plan:
            execution_plan = ["research", "technical", "news", "report"]

        # Ensure report is in execution_plan
        if "report" not in execution_plan:
            execution_plan.append("report")

        return {
            "companies": companies,
            "execution_plan": execution_plan,
        }
    except Exception as e:
        logger.error(f"Planner Agent parsing error: {e}. Using fallback plan.")
        return {
            "companies": ["Apple"],
            "execution_plan": ["research", "technical", "news", "report"],
        }