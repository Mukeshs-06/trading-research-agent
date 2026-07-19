from fastapi import APIRouter, HTTPException
from api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    HealthStatus,
    ToolInfo,
    AgentInfo,
)
from graph.workflow import graph
from tools.registry import TOOLS
from core.constants import DEFAULT_MODEL, AGENT_ROLES
from memory.conversation import memory_store
from core.logger import logger

router = APIRouter()

@router.get("/health", response_model=HealthStatus)
def health_check():
    """
    Returns system status and model parameters.
    """
    return HealthStatus(
        status="healthy",
        version="1.0.0",
        model=DEFAULT_MODEL,
    )

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_stocks(request: AnalyzeRequest):
    """
    Executes the multi-agent graph workflow for a user stock analysis query.
    """
    try:
        logger.info(f"API /analyze received request: '{request.user_request}'")
        initial_state = {
            "user_request": request.user_request,
            "companies": [],
            "execution_plan": [],
            "current_step": 0,
            "execution_trace": [],
            "timings": {},
            "errors": [],
        }

        final_state = graph.invoke(initial_state)

        # Store in conversation memory
        memory_store.add_entry(
            user_request=request.user_request,
            companies=final_state.get("companies", []),
            report_summary=final_state.get("report", ""),
            trace=final_state.get("execution_trace", []),
        )

        return AnalyzeResponse(
            user_request=request.user_request,
            companies=final_state.get("companies", []),
            execution_plan=final_state.get("execution_plan", []),
            report=final_state.get("report", "No report generated."),
            execution_trace=final_state.get("execution_trace", []),
            timings=final_state.get("timings", {}),
            reflection=final_state.get("reflection"),
            critic=final_state.get("critic"),
            errors=final_state.get("errors", []),
        )
    except Exception as e:
        logger.error(f"API /analyze error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools")
def list_tools():
    """
    Returns list of registered tools and their descriptions.
    """
    return [
        ToolInfo(name=tool.name, description=tool.description.strip())
        for tool in TOOLS
    ]

@router.get("/agents")
def list_agents():
    """
    Returns list of registered specialized agents.
    """
    descriptions = {
        "planner": "Creates an optimal execution plan for user queries.",
        "research": "Collects and synthesizes fundamental financial metrics.",
        "news": "Aggregates news headlines and performs LLM sentiment reasoning.",
        "technical": "Calculates RSI, MACD, Moving Averages, and Trend direction.",
        "report": "Generates a structured, factual equity research report.",
        "reflection": "Audits report completeness and requests revisions if needed.",
        "critic": "Audits report for hallucinations, contradictions, and compliance.",
    }
    return [
        AgentInfo(role=role, description=descriptions.get(role, "Specialized Agent"))
        for role in AGENT_ROLES
    ]

@router.get("/history")
def get_history():
    """
    Returns recent conversation memory history.
    """
    return memory_store.get_recent_history()
