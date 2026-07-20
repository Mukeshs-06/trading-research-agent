import operator
from typing import Annotated, TypedDict, List, Dict, Any, Optional

def merge_dict(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    res = a.copy() if a else {}
    if b:
        res.update(b)
    return res

def merge_list(a: List[Any], b: List[Any]) -> List[Any]:
    res = list(a) if a else []
    if b:
        for item in b:
            if item not in res:
                res.append(item)
    return res

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
    stock_data: Annotated[Dict[str, Any], merge_dict]
    technical_data: Annotated[Dict[str, Any], merge_dict]
    news_data: Annotated[Dict[str, Any], merge_dict]
    research_summary: str
    technical_summary: str
    news_summary: str
    report: str
    reflection: Dict[str, Any]
    critic: Dict[str, Any]
    revision_count: int
    human_approved: Optional[bool]
    human_feedback: Optional[str]
    execution_trace: Annotated[List[Dict[str, Any]], merge_list]
    timings: Annotated[Dict[str, float], merge_dict]
    errors: Annotated[List[str], merge_list]
    metadata: Dict[str, Any]