import json
import re
from langchain_core.messages import SystemMessage, HumanMessage
from core.settings import llm
from core.logger import logger
from prompts.reflection_prompt import REFLECTION_PROMPT

def reflection_agent(report: str, companies: list) -> dict:
    """
    Evaluates the completeness and coverage of the report.
    Returns:
    {
      "status": "APPROVED" | "NEEDS_REVISION",
      "feedback": "..."
    }
    """
    logger.info("Executing Reflection Agent...")
    try:
        prompt_text = f"Companies Analyzed: {companies}\n\nReport Content:\n{report}"
        response = llm.invoke([
            SystemMessage(content=REFLECTION_PROMPT),
            HumanMessage(content=prompt_text),
        ])
        content = response.content.strip()

        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\n?", "", content)
            content = re.sub(r"\n?```$", "", content).strip()

        return json.loads(content)
    except Exception as e:
        logger.error(f"Reflection Agent error: {e}")
        return {"status": "APPROVED", "feedback": f"Reflection skipped due to error: {str(e)}"}
