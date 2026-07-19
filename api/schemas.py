from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AnalyzeRequest(BaseModel):
    user_request: str = Field(
        ...,
        description="The research query or stock analysis request",
        json_schema_extra={"example": "Analyze Apple and Microsoft fundamentals and technicals"}
    )

class ExecutionTraceItemSchema(BaseModel):
    step: str
    status: str
    duration_seconds: float
    tools_called: List[str]
    details: Optional[str] = None

class AnalyzeResponse(BaseModel):
    user_request: str
    companies: List[str]
    execution_plan: List[str]
    report: str
    execution_trace: List[ExecutionTraceItemSchema]
    timings: Dict[str, float]
    reflection: Optional[Dict[str, Any]] = None
    critic: Optional[Dict[str, Any]] = None
    errors: List[str] = []

class ToolInfo(BaseModel):
    name: str
    description: str

class AgentInfo(BaseModel):
    role: str
    description: str

class HealthStatus(BaseModel):
    status: str
    version: str
    model: str
