from langchain_core.messages import SystemMessage, HumanMessage
from core.settings import llm
from core.logger import logger
from prompts.report_prompt import REPORT_PROMPT

def _format_raw_data_summary(raw_data: dict) -> str:
    """
    Formats raw data concisely to ensure token usage stays well within API rate limits.
    """
    if not isinstance(raw_data, dict):
        return str(raw_data)[:1500]

    lines = []
    stock = raw_data.get("stock", {})
    tech = raw_data.get("technical", {})
    news = raw_data.get("news", {})

    all_companies = set(list(stock.keys()) + list(tech.keys()) + list(news.keys()))

    for company in sorted(list(all_companies)):
        s_info = stock.get(company, {})
        t_info = tech.get(company, {})
        n_info = news.get(company, [])

        lines.append(f"=== {company} ===")
        if isinstance(s_info, dict) and "error" not in s_info:
            lines.append(f"Price: ${s_info.get('current_price', 'N/A')}, P/E: {s_info.get('pe_ratio', 'N/A')}, Market Cap: {s_info.get('market_cap', 'N/A')}")

        if isinstance(t_info, dict) and "error" not in t_info:
            lines.append(f"SMA20: {t_info.get('SMA20')}, SMA50: {t_info.get('SMA50')}, RSI: {t_info.get('RSI')}, MACD: {t_info.get('MACD')}, Trend: {t_info.get('Trend')}, Support: {t_info.get('Support_6M')}, Resistance: {t_info.get('Resistance_6M')}")

        if isinstance(n_info, list) and n_info:
            headlines = [f"• {item.get('title')}" for item in n_info[:3] if isinstance(item, dict) and item.get("title")]
            lines.append("Headlines:\n" + "\n".join(headlines))

        lines.append("")

    return "\n".join(lines)[:3500]

def report_agent(
    user_request: str,
    companies: list,
    research_summary: str,
    technical_summary: str,
    news_summary: str,
    raw_data: dict,
    reflection_feedback: str = "",
    tools_executed: list = None,
) -> str:
    """
    Synthesizes research, technical, and news insights into a final Markdown Equity Research Report.
    """
    logger.info("Executing Report Agent...")
    try:
        raw_summary_text = _format_raw_data_summary(raw_data)
        context_parts = [
            f"User Request: {user_request}",
            f"Target Companies: {', '.join(companies)}",
            f"--- Fundamental Research Synthesis ---\n{research_summary[:2000]}",
            f"--- Technical Analysis Synthesis ---\n{technical_summary[:2000]}",
            f"--- News & Sentiment Synthesis ---\n{news_summary[:2000]}",
            f"--- Concise Raw Data Metrics ---\n{raw_summary_text}",
        ]

        if reflection_feedback:
            context_parts.append(f"--- Reflection Audit Feedback to Address in Revision ---\n{reflection_feedback}")

        full_prompt = "\n\n".join(context_parts)

        response = llm.invoke([
            SystemMessage(content=REPORT_PROMPT),
            HumanMessage(content=full_prompt),
        ])

        report_markdown = response.content

        # Append Atomic Tools Used footer for transparency
        if tools_executed:
            unique_tools = sorted(list(set(tools_executed)))
            footer = "\n\n---\n### 🛠️ Atomic Tools Executed\n" + "\n".join([f"- `✓ {t}`" for t in unique_tools])
            report_markdown += footer

        return report_markdown
    except Exception as e:
        logger.error(f"Report Agent execution error: {e}")
        return f"# Error Generating Report\n\nFailed to generate report: {str(e)}"
