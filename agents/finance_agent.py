"""
Backwards-compatibility wrapper for finance_agent.
Refers directly to report_agent.
"""
from agents.report_agent import report_agent

def analyze_stock(stock_data: dict, news: list) -> str:
    companies = list(stock_data.keys()) if isinstance(stock_data, dict) else ["Company"]
    return report_agent(
        user_request="Stock Analysis Request",
        companies=companies,
        research_summary=str(stock_data),
        technical_summary="N/A",
        news_summary=str(news),
        raw_data={"stock": stock_data, "news": news},
    )