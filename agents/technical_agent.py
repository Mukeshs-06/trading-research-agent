from langchain_core.messages import SystemMessage, HumanMessage
from core.settings import llm
from core.logger import logger
from prompts.technical_prompt import TECHNICAL_PROMPT

def technical_agent(technical_data: dict) -> str:
    """
    Interprets technical indicators, momentum, trends, support and resistance.
    """
    logger.info("Executing Technical Agent...")
    try:
        prompt_text = f"Interpret the following technical indicators:\n\n{technical_data}"
        response = llm.invoke([
            SystemMessage(content=TECHNICAL_PROMPT),
            HumanMessage(content=prompt_text),
        ])
        return response.content
    except Exception as e:
        logger.error(f"Technical Agent execution error: {e}")
        return f"Error analyzing technicals: {str(e)}"
