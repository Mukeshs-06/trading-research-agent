from langchain_core.messages import SystemMessage, HumanMessage
from core.settings import llm
from core.logger import logger
from prompts.research_prompt import RESEARCH_PROMPT

def research_agent(stock_data: dict) -> str:
    """
    Analyzes company fundamental metrics and synthesizes business observations.
    """
    logger.info("Executing Research Agent...")
    try:
        prompt_text = f"Analyze the following stock fundamentals:\n\n{stock_data}"
        response = llm.invoke([
            SystemMessage(content=RESEARCH_PROMPT),
            HumanMessage(content=prompt_text),
        ])
        return response.content
    except Exception as e:
        logger.error(f"Research Agent execution error: {e}")
        return f"Error analyzing fundamentals: {str(e)}"
