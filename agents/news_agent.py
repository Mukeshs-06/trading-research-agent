from langchain_core.messages import SystemMessage, HumanMessage
from core.settings import llm
from core.logger import logger
from prompts.news_prompt import NEWS_PROMPT

def news_agent(news_data: dict) -> str:
    """
    Summarizes news headlines, assesses business impact, and determines sentiment via LLM reasoning.
    """
    logger.info("Executing News Agent...")
    try:
        prompt_text = f"Analyze the following recent news headlines:\n\n{news_data}"
        response = llm.invoke([
            SystemMessage(content=NEWS_PROMPT),
            HumanMessage(content=prompt_text),
        ])
        return response.content
    except Exception as e:
        logger.error(f"News Agent execution error: {e}")
        return f"Error analyzing news: {str(e)}"
