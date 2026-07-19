from typing import TypedDict, List, Dict, Any, Optional

class ExecutionTraceItem(TypedDict):
    step: str
    status: str
    duration_seconds: float
    tools_called: List[str]
    details: Optional[str]

class GraphState(TypedDict, total=False):
    user_request: str
    companies: List[str]
    execution_plan: List[str]
    current_step: int
    stock_data: Dict[str, Any]
    technical_data: Dict[str, Any]
    news_data: Dict[str, Any]
    research_summary: str
    technical_summary: str
    news_summary: str
    report: str
    reflection: Dict[str, Any]
    critic: Dict[str, Any]
    revision_count: int
    human_approved: Optional[bool]
    human_feedback: Optional[str]
    execution_trace: List[Dict[str, Any]]
    timings: Dict[str, float]
    errors: List[str]
    metadata: Dict[str, Any]