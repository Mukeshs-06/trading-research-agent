from langchain_core.messages import SystemMessage, HumanMessage
from core.settings import llm
from core.logger import logger
from prompts.report_prompt import REPORT_PROMPT

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
        context_parts = [
            f"User Request: {user_request}",
            f"Target Companies: {', '.join(companies)}",
            f"--- Fundamental Research Synthesis ---\n{research_summary}",
            f"--- Technical Analysis Synthesis ---\n{technical_summary}",
            f"--- News & Sentiment Synthesis ---\n{news_summary}",
            f"--- Raw Financial Data ---\n{raw_data}",
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
