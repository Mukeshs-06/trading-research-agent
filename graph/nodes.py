import time
from core.logger import logger
from tools.utility.company_resolver import resolve_company
from tools.financial.stock_tool import get_stock_data
from tools.financial.technical_tool import technical_analysis
from tools.market.news_tool import get_company_news

from agents.planner_agent import planner_agent
from agents.research_agent import research_agent
from agents.technical_agent import technical_agent
from agents.news_agent import news_agent
from agents.report_agent import report_agent
from agents.reflection_agent import reflection_agent
from agents.critic_agent import critic_agent

def _init_trace(state):
    if "execution_trace" not in state or state["execution_trace"] is None:
        state["execution_trace"] = []
    if "timings" not in state or state["timings"] is None:
        state["timings"] = {}
    if "errors" not in state or state["errors"] is None:
        state["errors"] = []
    if "revision_count" not in state:
        state["revision_count"] = 0
    return state

def planner_node(state):
    """
    Planner Node: Invokes Planner Agent to parse query and set execution plan.
    """
    state = _init_trace(state)
    start_t = time.time()
    logger.info("Executing Planner Node...")

    plan = planner_agent(state.get("user_request", ""))
    state["companies"] = plan["companies"]
    state["execution_plan"] = plan["execution_plan"]
    state["current_step"] = 0

    duration = round(time.time() - start_t, 2)
    state["timings"]["planner"] = duration
    state["execution_trace"].append({
        "step": "planner",
        "status": "completed",
        "duration_seconds": duration,
        "tools_called": [],
        "details": f"Planned companies: {plan['companies']}, execution plan: {plan['execution_plan']}"
    })
    return state

def research_node(state):
    """
    Research Node: Directly orchestrates resolve_company and get_stock_data atomic tools,
    then calls Research Agent for fundamental synthesis.
    """
    state = _init_trace(state)
    start_t = time.time()
    logger.info("Executing Research Node...")
    tools_called = ["resolve_company", "get_stock_data"]

    stock_data = {}
    companies = state.get("companies", [])

    for company in companies:
        ticker = resolve_company.invoke({"company_name": company})
        data = get_stock_data.invoke({"ticker": ticker})
        stock_data[company] = data

    state["stock_data"] = stock_data
    summary = research_agent(stock_data)
    state["research_summary"] = summary

    duration = round(time.time() - start_t, 2)
    state["timings"]["research"] = duration
    state["execution_trace"].append({
        "step": "research",
        "status": "completed",
        "duration_seconds": duration,
        "tools_called": tools_called,
        "details": f"Fetched fundamental data for {len(companies)} company/companies"
    })
    return state

def technical_node(state):
    """
    Technical Node: Directly orchestrates resolve_company and technical_analysis atomic tools,
    then calls Technical Agent for indicator interpretation.
    """
    state = _init_trace(state)
    start_t = time.time()
    logger.info("Executing Technical Node...")
    tools_called = ["resolve_company", "technical_analysis"]

    tech_data = {}
    companies = state.get("companies", [])

    for company in companies:
        ticker = resolve_company.invoke({"company_name": company})
        data = technical_analysis.invoke({"ticker": ticker})
        tech_data[company] = data

    state["technical_data"] = tech_data
    summary = technical_agent(tech_data)
    state["technical_summary"] = summary

    duration = round(time.time() - start_t, 2)
    state["timings"]["technical"] = duration
    state["execution_trace"].append({
        "step": "technical",
        "status": "completed",
        "duration_seconds": duration,
        "tools_called": tools_called,
        "details": f"Calculated technical indicators for {len(companies)} company/companies"
    })
    return state

def news_node(state):
    """
    News Node: Directly orchestrates get_company_news atomic tool,
    then calls News Agent for news synthesis and LLM sentiment analysis.
    """
    state = _init_trace(state)
    start_t = time.time()
    logger.info("Executing News Node...")
    tools_called = ["get_company_news"]

    news_data = {}
    companies = state.get("companies", [])

    for company in companies:
        items = get_company_news.invoke({"company_name": company})
        news_data[company] = items

    state["news_data"] = news_data
    summary = news_agent(news_data)
    state["news_summary"] = summary

    duration = round(time.time() - start_t, 2)
    state["timings"]["news"] = duration
    state["execution_trace"].append({
        "step": "news",
        "status": "completed",
        "duration_seconds": duration,
        "tools_called": tools_called,
        "details": f"Retrieved headlines for {len(companies)} company/companies"
    })
    return state

def report_node(state):
    """
    Report Node: Calls Report Agent to generate synthesized markdown report.
    """
    state = _init_trace(state)
    start_t = time.time()
    logger.info("Executing Report Node...")

    # Gather all tools executed so far in execution_trace
    executed_tools = []
    for item in state.get("execution_trace", []):
        executed_tools.extend(item.get("tools_called", []))

    feedback = state.get("reflection", {}).get("feedback", "")
    if state.get("human_feedback"):
        feedback += f"\nHuman Feedback: {state['human_feedback']}"

    report_text = report_agent(
        user_request=state.get("user_request", ""),
        companies=state.get("companies", []),
        research_summary=state.get("research_summary", "Fundamental research was not requested for this query."),
        technical_summary=state.get("technical_summary", "Technical indicators were not requested for this query."),
        news_summary=state.get("news_summary", "News search was not requested for this query."),
        raw_data={
            "stock": state.get("stock_data", {}),
            "technical": state.get("technical_data", {}),
            "news": state.get("news_data", {}),
        },
        reflection_feedback=feedback,
        tools_executed=executed_tools,
    )
    state["report"] = report_text

    duration = round(time.time() - start_t, 2)
    state["timings"]["report"] = duration
    state["execution_trace"].append({
        "step": "report",
        "status": "completed",
        "duration_seconds": duration,
        "tools_called": [],
        "details": "Generated synthesized Markdown report"
    })
    return state

def reflection_node(state):
    """
    Reflection Node: Optional evaluation of report completeness.
    """
    state = _init_trace(state)
    start_t = time.time()
    logger.info("Executing Reflection Node...")

    reflection = reflection_agent(
        report=state.get("report", ""),
        companies=state.get("companies", [])
    )
    state["reflection"] = reflection

    duration = round(time.time() - start_t, 2)
    state["timings"]["reflection"] = duration
    state["execution_trace"].append({
        "step": "reflection",
        "status": "completed",
        "duration_seconds": duration,
        "tools_called": [],
        "details": f"Reflection Status: {reflection.get('status', 'APPROVED')}"
    })
    return state

def critic_node(state):
    """
    Critic Node: Fast audit for hallucinations & compliance.
    """
    state = _init_trace(state)
    start_t = time.time()
    logger.info("Executing Critic Node...")

    critic = critic_agent(
        report=state.get("report", ""),
        raw_data={
            "stock": state.get("stock_data", {}),
            "technical": state.get("technical_data", {}),
            "news": state.get("news_data", {}),
        }
    )
    state["critic"] = critic

    duration = round(time.time() - start_t, 2)
    state["timings"]["critic"] = duration
    state["execution_trace"].append({
        "step": "critic",
        "status": "completed",
        "duration_seconds": duration,
        "tools_called": [],
        "details": f"Critic Audit Status: {critic.get('status', 'APPROVED')}"
    })
    return state